# zip()

products = ["Coffee", "Croissant", "Tea"]
prices = [250, 150, 100]

for item, price in zip(products, prices):
    print(f"Order: {item} costs ${price}")

menu = dict(zip(products, prices))



# enumerate()

tasks = ["have a breakfast", "read documentation", "practice C++"]

for index, task in enumerate(tasks, start=1):
    print(f"{index}. {task}")