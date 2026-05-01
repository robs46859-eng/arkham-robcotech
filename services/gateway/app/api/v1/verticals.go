package v1

import (
	"encoding/json"
	"net/http"
)

// --- SaaS Vertical Handlers ---

// HandleSaaSBudgetVariance handles POST /v1/saas/budget-variance
func HandleSaaSBudgetVariance(w http.ResponseWriter, r *http.Request) {
	var body struct {
		ProjectID string `json:"project_id"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error": "invalid request body"}`, http.StatusBadRequest)
		return
	}

	TriggerWorkflow(w, r, "budget_variance_analysis", map[string]interface{}{
		"project_id": body.ProjectID,
		"vertical":   "saas",
	})
}

// HandleSaaSBoardDeck handles POST /v1/saas/board-deck
func HandleSaaSBoardDeck(w http.ResponseWriter, r *http.Request) {
	TriggerWorkflow(w, r, "board_deck_generation", map[string]interface{}{
		"vertical": "saas",
	})
}

// --- Ecommerce Vertical Handlers ---

// HandleEcomInventory handles POST /v1/ecom/inventory
func HandleEcomInventory(w http.ResponseWriter, r *http.Request) {
	var body struct {
		InventorySignals []map[string]interface{} `json:"inventory_signals"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error": "invalid request body"}`, http.StatusBadRequest)
		return
	}

	TriggerWorkflow(w, r, "ecom_inventory_monitor", map[string]interface{}{
		"inventory_signals": body.InventorySignals,
	})
}

// HandleEcomSignals handles POST /v1/ecom/signals
func HandleEcomSignals(w http.ResponseWriter, r *http.Request) {
	var body struct {
		ChannelSignals map[string]interface{} `json:"channel_signals"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error": "invalid request body"}`, http.StatusBadRequest)
		return
	}

	TriggerWorkflow(w, r, "ecom_cart_recovery", map[string]interface{}{
		"channel_signals": body.ChannelSignals,
	})
}

// --- Staffing Vertical Handlers ---

// HandleStaffingAudit handles POST /v1/staffing/audit
func HandleStaffingAudit(w http.ResponseWriter, r *http.Request) {
	TriggerWorkflow(w, r, "staffing-placement-audit", map[string]interface{}{})
}

// HandleStaffingVelocity handles POST /v1/staffing/velocity
func HandleStaffingVelocity(w http.ResponseWriter, r *http.Request) {
	TriggerWorkflow(w, r, "staffing-pipeline-velocity", map[string]interface{}{})
}

// --- Media Vertical Handlers (Standardizing with others) ---

// HandleMediaVelocity handles POST /v1/media/velocity
func HandleMediaVelocity(w http.ResponseWriter, r *http.Request) {
	TriggerWorkflow(w, r, "media-content-velocity", map[string]interface{}{})
}

// HandleMediaEPC handles POST /v1/media/epc
func HandleMediaEPC(w http.ResponseWriter, r *http.Request) {
	TriggerWorkflow(w, r, "media-epc-monitor", map[string]interface{}{})
}
