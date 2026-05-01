// Gateway route to Media & Commerce service
package v1

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
	"os"
)

// MediaCommerceServiceURL is the media-commerce service URL
var MediaCommerceServiceURL = os.Getenv("MEDIA_COMMERCE_URL")

func init() {
	if MediaCommerceServiceURL == "" {
		MediaCommerceServiceURL = "http://media-commerce:8087"
	}
}

// ProxyToMediaCommerce proxies requests to the media-commerce service
func ProxyToMediaCommerce(w http.ResponseWriter, r *http.Request, path string) {
	// Build upstream URL
	upstreamURL := MediaCommerceServiceURL + "/api/v1" + path

	// Read request body
	var body io.Reader
	if r.Method == "POST" || r.Method == "PUT" {
		body = r.Body
	}

	// Create upstream request
	req, err := http.NewRequestWithContext(r.Context(), r.Method, upstreamURL, body)
	if err != nil {
		http.Error(w, `{"error": "failed to create upstream request"}`, http.StatusInternalServerError)
		return
	}

	// Copy headers
	for key, values := range r.Header {
		for _, value := range values {
			req.Header.Add(key, value)
		}
	}

	// Execute request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		http.Error(w, `{"error": "failed to reach media-commerce service"}`, http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	// Copy response headers
	for key, values := range resp.Header {
		for _, value := range values {
			w.Header().Add(key, value)
		}
	}

	// Copy status code
	w.WriteHeader(resp.StatusCode)

	// Copy response body
	io.Copy(w, resp.Body)
}

// ContentStrategyRequest represents a content strategy request
type ContentStrategyRequest struct {
	TenantID string `json:"tenant_id"`
	Vertical string `json:"vertical"`
	Topic    string `json:"topic"`
}

// HandleContentStrategy handles POST /v1/content/strategy
func HandleContentStrategy(w http.ResponseWriter, r *http.Request) {
	var req ContentStrategyRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error": "invalid request body"}`, http.StatusBadRequest)
		return
	}

	// Proxy to media-commerce service
	body, _ := json.Marshal(req)
	r.Body = io.NopCloser(bytes.NewReader(body))
	ProxyToMediaCommerce(w, r, "/content/strategy")
}

// HandleLeadRouting handles POST /v1/leads/route
func HandleLeadRouting(w http.ResponseWriter, r *http.Request) {
	// Proxy to media-commerce service
	ProxyToMediaCommerce(w, r, "/leads/route")
}

// HandleEPCMonitor handles POST /v1/epc/monitor
func HandleEPCMonitor(w http.ResponseWriter, r *http.Request) {
	// Proxy to media-commerce service
	ProxyToMediaCommerce(w, r, "/epc/monitor")
}

// HandleExecutiveBriefing handles GET /v1/executive/briefing
func HandleExecutiveBriefing(w http.ResponseWriter, r *http.Request) {
	// Proxy to media-commerce service
	ProxyToMediaCommerce(w, r, "/executive/briefing")
}
