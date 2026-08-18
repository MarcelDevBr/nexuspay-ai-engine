# -----------------------------------------------------------------------------
# AWS Budgets: FinOps Guardrail para Custo Zero / Free Tier
# Dispara alerta caso o gasto na conta atinja $0.80 ou $1.00
# -----------------------------------------------------------------------------
resource "aws_budgets_budget" "finops_zero_cost_guard" {
  count             = var.is_localstack ? 0 : 1
  name              = "nexuspay-monthly-budget-guard"
  budget_type       = "COST"
  limit_amount      = "1.00"
  limit_unit        = "USD"
  time_unit         = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.alert_email]
  }
}
