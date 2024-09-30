from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'
    
    def ready(self):
        import dashboard.dash_apps
        import dashboard.dash_apps.business_licenses_monthly
        import dashboard.dash_apps.business_licenses_distribution
        import dashboard.dash_apps.business_licenses_renewals
        import dashboard.dash_apps.business_licenses_histogram
        import dashboard.dash_apps.business_licenses_avg_length
        import dashboard.dash_apps.business_licenses_map
