package v1

import (
	"encoding/json"
	"io"
	"net/http"
	"os"
)

// StudioServiceURL is the studio vertical service URL (if split out)
// For now, it defaults to the orchestration service which hosts the tasks.
var StudioServiceURL = os.Getenv("STUDIO_URL")

func init() {
	if StudioServiceURL == "" {
		if os.Getenv("ORCHESTRATION_URL") != "" {
			StudioServiceURL = os.Getenv("ORCHESTRATION_URL")
		} else {
			StudioServiceURL = "http://orchestration:8083"
		}
	}
}

// ProxyToStudio proxies requests to the studio vertical logic
func ProxyToStudio(w http.ResponseWriter, r *http.Request, path string) {
	upstreamURL := StudioServiceURL + "/api/v1" + path

	var body io.Reader
	if r.Method == "POST" || r.Method == "PUT" {
		body = r.Body
	}

	req, err := http.NewRequestWithContext(r.Context(), r.Method, upstreamURL, body)
	if err != nil {
		http.Error(w, `{"error": "failed to create studio request"}`, http.StatusInternalServerError)
		return
	}

	for key, values := range r.Header {
		for _, value := range values {
			req.Header.Add(key, value)
		}
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		http.Error(w, `{"error": "failed to reach studio vertical service"}`, http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	for key, values := range resp.Header {
		for _, value := range values {
			w.Header().Add(key, value)
		}
	}

	w.WriteHeader(resp.StatusCode)
	io.Copy(w, resp.Body)
}

// HandleStudioDeliveryPosture handles POST /v1/studio/delivery-posture
func HandleStudioDeliveryPosture(w http.ResponseWriter, r *http.Request) {
	var body struct {
		ProjectID string `json:"project_id"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error": "invalid request body"}`, http.StatusBadRequest)
		return
	}

	// For now, we route this as a workflow trigger to Orchestration
	inputData := map[string]interface{}{
		"project_id": body.ProjectID,
	}
	TriggerWorkflow(w, r, "studio_delivery_posture", inputData)
}

// HandleStudioProjectVelocity handles POST /v1/studio/project-velocity
func HandleStudioProjectVelocity(w http.ResponseWriter, r *http.Request) {
	var body struct {
		ProjectID string `json:"project_id"`
		TimeRange string `json:"time_range"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error": "invalid request body"}`, http.StatusBadRequest)
		return
	}

	inputData := map[string]interface{}{
		"project_id": body.ProjectID,
		"time_range": body.TimeRange,
	}
	TriggerWorkflow(w, r, "studio_project_velocity", inputData)
}
