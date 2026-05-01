package v1

import (
	"bytes"
	"encoding/json"
	"net/http"
	"os"
)

// OrchestrationURL is the orchestration service URL
var OrchestrationURL = os.Getenv("ORCHESTRATION_URL")

func init() {
	if OrchestrationURL == "" {
		OrchestrationURL = "http://orchestration:8083"
	}
}

// TriggerWorkflow sends a request to trigger an Arkham workflow
func TriggerWorkflow(w http.ResponseWriter, r *http.Request, flowType string, inputData map[string]interface{}) {
	tenantID := r.Header.Get("X-Tenant-ID")
	if tenantID == "" {
		tenantID = "default"
	}

	payload := map[string]interface{}{
		"workflow_type": flowType,
		"tenant_id":     tenantID,
		"input_data":    inputData,
	}

	jsonPayload, _ := json.Marshal(payload)
	req, err := http.NewRequestWithContext(r.Context(), "POST", OrchestrationURL+"/api/v1/workflows", bytes.NewBuffer(jsonPayload))
	if err != nil {
		http.Error(w, `{"error": "failed to create workflow request"}`, http.StatusInternalServerError)
		return
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		http.Error(w, `{"error": "failed to trigger orchestration"}`, http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(resp.StatusCode)
	var result map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&result)
	json.NewEncoder(w).Encode(result)
}

// HandleMaternalIngestion handles automated ingestion of maternal resources
func HandleMaternalIngestion(w http.ResponseWriter, r *http.Request) {
	var body struct {
		SourceURL string `json:"source_url"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error": "invalid request body"}`, http.StatusBadRequest)
		return
	}

	TriggerWorkflow(w, r, "maternal_resource_ingestion", map[string]interface{}{
		"source_url": body.SourceURL,
	})
}

// HandleMaternalVerification handles verification of maternal-friendly places
func HandleMaternalVerification(w http.ResponseWriter, r *http.Request) {
	var body struct {
		PlaceData map[string]interface{} `json:"place_data"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error": "invalid request body"}`, http.StatusBadRequest)
		return
	}

	TriggerWorkflow(w, r, "maternal_place_verification_loop", map[string]interface{}{
		"place_data": body.PlaceData,
	})
}

// HandlePregnancyJourney handles intelligent pregnancy journey analysis
func HandlePregnancyJourney(w http.ResponseWriter, r *http.Request) {
	var body struct {
		WeekNumber int      `json:"week_number"`
		Symptoms   []string `json:"symptoms"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error": "invalid request body"}`, http.StatusBadRequest)
		return
	}

	TriggerWorkflow(w, r, "pregnancy_journey_advisory", map[string]interface{}{
		"week_number": body.WeekNumber,
		"symptoms":    body.Symptoms,
	})
}
