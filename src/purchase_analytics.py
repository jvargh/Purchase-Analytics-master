import csv

# Get Order_Products CSV into Dictionary. Product_id as key
orders = {}
with open('../input/order_products.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        orders[row["product_id"]] = [row["order_id"], row["add_to_cart_order"], row["reordered"] ]

# Get Products CSV into Dictionary. Product_id as key
products = {}
with open('../input/products.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        products[row["product_id"]] = [row["product_name"], row["aisle_id"], row["department_id"] ]

# Create Department map for final output
dept={}
for productId in products:
    deptId = products[productId][2]
    # A department_id should be listed only if number_of_orders is greater than 0
    if productId in orders:
        # Init new entry if none exists for Product Id
        if deptId not in dept:
            dept[deptId] = {"department_id": int(deptId),
                            "number_of_orders": 0,
                            "number_of_first_orders": 0,
                            "percentage": 0.00}
        row = dept[deptId]
        row["number_of_orders"] += 1
        # XOR logic used for 1+ products
        row["number_of_first_orders"] = int(row["number_of_first_orders"]) ^ int(orders[productId][2])
        # percentage should be rounded to the second decimal
        row["percentage"] = "{:0.2f}".format(row["number_of_first_orders"]/row["number_of_orders"])

# Same as above but XOR logic used when Number_Of_Orders=1
for productId in products:
    deptId = products[productId][2]
    if productId in orders and deptId in dept:
        row = dept[deptId]
        if row["number_of_orders"] == 1:
            row["number_of_first_orders"] ^= 1
            row["percentage"] = "{:0.2f}".format(row["number_of_first_orders"] / row["number_of_orders"])

# List of dictionary entries
listDept= [v for v in dept.values()]
# listed in ascending order by department_id
listDept.sort(key=lambda k : k['department_id'])
print(listDept)

# Write dictionary to Output CSV file
with open('../output/report.csv','w+',newline='') as csv_file:
    fc = csv.DictWriter(csv_file, fieldnames=listDept[0].keys())
    fc.writeheader()
    fc.writerows(listDept)

