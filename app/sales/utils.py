from app import app, db
from sqlalchemy import text


def generate_report(date):
    with app.app_context():
        session = db.session()
        # query = '''SELECT (SELECT SUM(quantity) AS Total_items_sold FROM order_lines, orders WHERE  orders.id = order_lines.order_id AND orders.created_at = DATE(:date)),
        #             (SELECT COUNT(DISTINCT customer_id) AS Total_customers FROM orders WHERE DATE(orders.created_at) = DATE(:date)),
        #             (SELECT SUM(discounted_amount) AS Total_discount FROM order_lines, orders WHERE orders.created_at = DATE(:date)),
        #             (SELECT AVG(discount_rate)  AS Avg_discount FROM order_lines, orders WHERE  orders.id = order_lines.order_id AND DATE(orders.created_at) = DATE(:date)),
        #             (SELECT AVG(total_amount) AS Avg_order FROM order_lines, orders WHERE  orders.id = order_lines.order_id AND DATE(orders.created_at) = DATE(:date)),
        #             (SELECT SUM(rate*total_amount)/100 AS Total_commission FROM commissions, order_lines, orders WHERE commissions.vendor_id = orders.vendor_id AND DATE(commissions.date) = DATE(orders.created_at) AND DATE(orders.created_at)=DATE(:date)),
        #             (SELECT AVG(rate*total_amount)/100 AS Avg_commission FROM commissions, order_lines, orders WHERE commissions.vendor_id = orders.vendor_id AND DATE(commissions.date) = DATE(orders.created_at) AND DATE(orders.created_at)=DATE(:date))
        #             FROM commissions, orders, order_lines, product_promotions, promotions;'''
        # query1 ='''SELECT promotions.description, SUM(commissions.rate*order_lines.total_amount)/100 AS Commission_earned FROM commissions, orders, order_lines, product_promotions, promotions 
        #             WHERE commissions.vendor_id = orders.vendor_id 
        #             AND DATE(commissions.date) = DATE(orders.created_at)
        #             AND orders.id = order_lines.order_id 
        #             AND order_lines.product_id = product_promotions.product_id 
        #             AND product_promotions.promotion_id = promotions.id
        #             AND DATE(orders.created_at) = DATE(:date) 
        #             GROUP BY promotions.description);'''
        # result = session.execute(text(query), {'date': date})

        # print(result.fetchall())
        total_items_sold = session.execute(text('''SELECT SUM(quantity) FROM order_lines, orders WHERE  orders.id = order_lines.order_id AND DATE(orders.created_at) = DATE(:date);'''), {'date': date})
        total_customers = session.execute(text('''SELECT COUNT(DISTINCT customer_id) FROM orders WHERE DATE(orders.created_at) = DATE(:date);'''), {'date': date})
        total_discount = session.execute(text('''SELECT SUM(discounted_amount) FROM order_lines, orders WHERE DATE(orders.created_at) = DATE(:date);'''), {'date': date})
        avg_discount = session.execute(text('''SELECT AVG(discount_rate) FROM order_lines, orders WHERE  orders.id = order_lines.order_id AND DATE(orders.created_at) = DATE(:date);'''), {'date': date})
        avg_order = session.execute(text('''SELECT AVG(total_amount) FROM order_lines, orders WHERE  orders.id = order_lines.order_id AND DATE(orders.created_at) = DATE(:date);'''), {'date': date})
        total_commission = session.execute(text('''SELECT SUM(rate*total_amount)/100 FROM commissions, order_lines, orders WHERE commissions.vendor_id = orders.vendor_id AND DATE(commissions.date) = DATE(orders.created_at) AND DATE(orders.created_at)=DATE(:date);'''), {'date': date})
        commission_order_avg = session.execute(text('''SELECT AVG(rate*total_amount)/100 FROM commissions, order_lines, orders WHERE commissions.vendor_id = orders.vendor_id AND DATE(commissions.date) = DATE(orders.created_at) AND DATE(orders.created_at)=DATE(:date);'''), {'date': date})
        commissions_per_promotion = session.execute(text('''SELECT promotions.description, SUM(commissions.rate*order_lines.total_amount)/100 FROM commissions, orders, order_lines, product_promotions, promotions
        WHERE commissions.vendor_id = orders.vendor_id
                    AND DATE(commissions.date) = DATE(orders.created_at)
                    AND orders.id = order_lines.order_id
                    AND order_lines.product_id = product_promotions.product_id
                    AND product_promotions.promotion_id = promotions.id
                    AND DATE(orders.created_at) = DATE(:date)
                    GROUP BY promotions.description;'''), {'date': date})

        report = {
            'customers': total_customers.fetchone(),
            'total_discount_amount': total_discount.fetchall(),
            'items': total_items_sold.fetchall(),
            'order_total_avg': avg_order.fetchall(),
            'discount_rate_avg': avg_discount.fetchall(),
            'commissions': {
                'total': total_commission.fetchall(),
                'avg_commission_per_order': commission_order_avg.fetchall(),
                'commission_by_promotion': commissions_per_promotion.fetchall()
            }
        }
        session.close()
    return report
