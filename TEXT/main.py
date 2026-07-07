from fastapi import FastAPI
app = FastAPI()
mock_orders = [
{"id": 1, "customer_name": "Nguyen Van A", "total_amount": 500000, "status":
"delivered"},
{"id": 2, "customer_name": "Tran Thi B", "total_amount": 200000, "status":
"pending"},
{"id": 3, "customer_name": "Nguyen Van A", "total_amount": 350000, "status":
"delivered"},
{"id": 4, "customer_name": "Le Van C", "total_amount": 350000, "status":
"delivered"},
{"id": 5, "customer_name": "Tran Thi B", "total_amount": 500000, "status":
"delivered"},
{"id": 6, "customer_name": "Pham Van D", "total_amount": 150000, "status":
"cancelled"}]


@app.get("/orders/revenue-report")
def get_ordersrevenue_report():
    total_revenue = 0
    successful_revenue = 0
    average_order_value = 0 
    number = len(mock_orders)
    if not mock_orders:
        return{
            "total_revenue":0,
            "successful_revenue":0,
            "average_order_value":0

        }
    for i in mock_orders:
        total_revenue += i["total_amount"]
        if i["status"] == "delivered":
            successful_revenue += i["total_amount"]
    average_order_value = float(total_revenue / number)
    return{
            "total_revenue":total_revenue,
            "successful_revenue":successful_revenue,
            "average_order_value":average_order_value
        }

@app.get("/orders/status-breakdown")
def get_status_breakdown():
    pending = 0
    delivered = 0
    cancelled = 0
    for i in mock_orders:
        if i["status"] == "pending":
            pending += 1
        elif i["status"] == "delivered":
            delivered += 1
        else:
            cancelled += 1
    return {
        "breakdown":{
            "pending":pending,
            "delivered":delivered,
            "cancelled":cancelled
        }
    }

@app.get("/orders/top-customers")
def get_top_customers():
    list =[]
    for i in mock_orders:
        if i["status"] == "delivered":
            for y in list:
                if i["customer_name"] in y["customer_name"]:
                    y["total_amount"] += i["total_amount"]
        new_order_sort = {
            "customer_name" :i["customer_name"] ,
            "total_amount": i["total_amount"]
        }
        list.append(new_order_sort)
    if not list:
        return{
            "massage": "No VIP customers found"
        }
    limit = 3
    max = list[0]
    listsort = []
    num =0
    while True:
        if i["total_amount"] > max:
            listsort.append(i)
            num += 1
        if num > 3:
            break
    return {
        "top_customer": listsort
    }




    


        


        
