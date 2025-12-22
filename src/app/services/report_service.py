class ReportService:
    def __init__(self, report):
        self.report = report

    def get_rental_overview_report(self):

        return self.report.get_rental_overview()

    def get_rv_overview_report(self):

        return self.report.get_rv_overview()

    def get_revenue_by_brand_report(self):

        return self.report.get_revenue_by_brand()

    def get_customer_statistics_report(self):

        return self.report.get_customer_statistics()

    def get_popular_accessories_report(self):

        return self.report.get_popular_accessories()

    def get_rv_utilization_report(self):

        return self.report.get_rv_utilization()