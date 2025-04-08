
def get_common_path(path1, path2):
    return list(set(path1) & set(path2))

# Example robot paths
robotA = [1, 2, 3, 4, 5]
robotB = [10, 9, 5, 4, 3]

common_path = get_common_path(robotA, robotB)
print("🟨 Common path (aisle):", common_path)
