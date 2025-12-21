class Report:
  def __init__(self, db_connection):
      self.conn = db_connection.get_connection()

  def get_rental_overview(self):
      cursor = self.conn.cursor()

      sql = """
      SELECT * FROM v_rental_overview ORDER BY creation_date DESC
      """

      cursor.execute(sql)
      result = cursor.fetchall()
      cursor.close()
      return result

  def get_rv_overview(self):
      cursor = self.conn.cursor()

      sql = """
      SELECT * FROM v_rv_overview ORDER BY brand_name, spz
      """
      cursor.execute(sql)
      result = cursor.fetchall()
      cursor.close()
      return result

  def get_revenue_by_brand(self):
      cursor = self.conn.cursor()

      sql = """
      SELECT * FROM v_revenue_by_brand ORDER BY total_revenue DESC
      """
      cursor.execute(sql)
      result = cursor.fetchall()
      cursor.close()
      return result

  def get_customer_statistics(self):
      cursor = self.conn.cursor()

      sql = """
      SELECT * FROM v_customer_statistics ORDER BY total_spent DESC
      """
      cursor.execute(sql)
      result = cursor.fetchall()
      cursor.close()
      return result

  def get_popular_accessories(self):
      cursor = self.conn.cursor()

      sql = """
      SELECT * FROM v_popular_accessories ORDER BY  times_rented DESC
      """
      cursor.execute(sql)
      result = cursor.fetchall()
      cursor.close()
      return result

  def get_rv_utilization(self):
      cursor = self.conn.cursor()

      sql = """
      SELECT * FROM v_rv_utilization ORDER BY total_revenue DESC NULLS LAST
      """
      cursor.execute(sql)
      result = cursor.fetchall()
      cursor.close()
      return result
