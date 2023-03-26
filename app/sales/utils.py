from app import app, db
from sqlalchemy import text


def generate_report(date):
    with app.app_context():
        session = db.session()
        total_items_sold = session.execute(text('''SELECT SUM(quantity) FROM order_lines, orders WHERE  orders.id = order_lines.order_id AND DATE(orders.created_at) = DATE(:date);'''), {'date': date})
        total_customers = session.execute(text('''SELECT COUNT(DISTINCT customer_id) FROM orders WHERE DATE(orders.created_at) = DATE(:date);'''), {'date': date})
        total_discount = session.execute(text('''SELECT SUM(discounted_amount) FROM order_lines, orders WHERE DATE(orders.created_at) = DATE(:date);'''), {'date': date})
        avg_discount = session.execute(text('''SELECT AVG(discount_rate) FROM order_lines, orders WHERE  orders.id = order_lines.order_id AND DATE(orders.created_at) = DATE(:date);'''), {'date': date})
        avg_order = session.execute(text('''SELECT AVG(total_amount) FROM order_lines, orders WHERE  orders.id = order_lines.order_id AND DATE(orders.created_at) = DATE(:date);'''), {'date': date})
        total_commission = session.execute(text('''SELECT SUM(rate*total_amount)/100 FROM commissions, order_lines, orders WHERE commissions.vendor_id = orders.vendor_id AND DATE(commissions.date) = DATE(orders.created_at) AND DATE(orders.created_at)=DATE(:date);'''), {'date': date})
        commission_order_avg = session.execute(text('''SELECT AVG(rate*total_amount)/100 FROM commissions, order_lines, orders WHERE commissions.vendor_id = orders.vendor_id AND DATE(commissions.date) = DATE(orders.created_at) AND DATE(orders.created_at)=DATE(:date);'''), {'date': date})
        commissions_per_promotion = session.execute(text('''SELECT promotions.id, promotions.description, SUM(commissions.rate * order_lines.total_amount) AS commission_earned
                                                                FROM promotions
                                                                JOIN product_promotions ON promotions.id = product_promotions.promotion_id
                                                                JOIN order_lines ON product_promotions.product_id = order_lines.product_id
                                                                JOIN orders ON order_lines.order_id = orders.id
                                                                JOIN commissions ON orders.vendor_id = commissions.vendor_id AND commissions.date = '2023-03-26'
                                                                GROUP BY promotions.id, promotions.description'''), {'date': date})
        report = {}

        tc = total_customers.fetchone()
        if tc[0]:
            tc = int(tc[0])
        else:
            tc = 'null'
        td = total_discount.fetchone()
        if td[0]:
            td = int(td[0])
        else:
            td = 'null'
        ts = total_items_sold.fetchone()
        if ts[0]:
            ts = int(ts[0])
        else:
            ts = 'null'
        ao = avg_order.fetchone()
        if ao[0]:
            ao = int(ao[0])
        else:
            ao = 'null'
        ad = avg_discount.fetchone()
        if ad[0]:
            ad = int(ad[0])
        else:
            ad = 'null'
        tcomm = total_commission.fetchone()
        if tcomm[0]:
            tcomm = int(tcomm[0])
        else:
            tcomm = 'null'
        avgcomm = commission_order_avg.fetchone()
        if avgcomm[0]:
            avgcomm = int(avgcomm[0])
        else:
            avgcomm = 'null'
        comm_promo = commissions_per_promotion.fetchone()
        if comm_promo:
            comm_promo = int(comm_promo[0])
        report['customers'] = tc
        report['total_discount_amout'] = td
        report['items'] = ts
        report['order_total_avg'] = ao
        report['discount_rate_avg'] = ad
        report['commissions'] = {}
        report['commissions']['total'] = tcomm
        report['commissions']['avg_commission_per_order'] = avgcomm
        report['commissions']['commission_by_promotion'] = comm_promo
        session.close()
    return report
