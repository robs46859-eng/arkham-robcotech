package v1

import (
	"io"
	"net/http"
	"os"
)

// BillingServiceURL is the billing service URL inside the container app environment.
var BillingServiceURL = os.Getenv("BILLING_URL")

func init() {
	if BillingServiceURL == "" {
		BillingServiceURL = "http://billing:8080"
	}
}

// proxyToBilling forwards requests to the billing service without applying gateway auth.
func proxyToBilling(w http.ResponseWriter, r *http.Request, path string) {
	upstreamURL := BillingServiceURL + path

	var body io.Reader
	if r.Body != nil {
		body = r.Body
	}

	req, err := http.NewRequestWithContext(r.Context(), r.Method, upstreamURL, body)
	if err != nil {
		http.Error(w, `{"error": "failed to create upstream billing request"}`, http.StatusInternalServerError)
		return
	}

	for key, values := range r.Header {
		for _, value := range values {
			req.Header.Add(key, value)
		}
	}

	resp, err := (&http.Client{}).Do(req)
	if err != nil {
		http.Error(w, `{"error": "failed to reach billing service"}`, http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	for key, values := range resp.Header {
		for _, value := range values {
			w.Header().Add(key, value)
		}
	}

	w.WriteHeader(resp.StatusCode)
	_, _ = io.Copy(w, resp.Body)
}

// HandleStripeWebhook proxies the canonical Stripe webhook endpoint to billing.
func HandleStripeWebhook(w http.ResponseWriter, r *http.Request) {
	proxyToBilling(w, r, "/api/v1/stripe/webhook")
}

// HandleStripeWebhookLegacy keeps the old webhook path working during cutover.
func HandleStripeWebhookLegacy(w http.ResponseWriter, r *http.Request) {
	proxyToBilling(w, r, "/api/v1/billing/webhook")
}
