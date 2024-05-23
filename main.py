import random
import json
import time

class TreeNode:
    def __init__(self, value=0, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def count_leaves_and_height(node):
    if node is None:
        return 0, 0
    if node.left is None and node.right is None:
        return 1, 1
    left_count, left_height = count_leaves_and_height(node.left)
    right_count, right_height = count_leaves_and_height(node.right)
    total_leaves = left_count + right_count
    height = max(left_height, right_height) + 1
    return total_leaves, height


def find_subtrees_with_leaves(root, target_leaves):
    if root is None:
        return [], 0

    left_count, left_height = count_leaves_and_height(root.left)
    right_count, right_height = count_leaves_and_height(root.right)
    total_leaves = left_count + right_count

    if total_leaves == target_leaves:
        max_height = max(left_height, right_height)
        return [(root, total_leaves, max_height)], max_height

    left_subtrees, left_height = find_subtrees_with_leaves(root.left, target_leaves)
    right_subtrees, right_height = find_subtrees_with_leaves(root.right, target_leaves)

    subtrees = []
    if left_subtrees and left_height >= right_height:
        subtrees += left_subtrees
    if right_subtrees and right_height >= left_height:
        subtrees += right_subtrees

    return subtrees, max(left_height, right_height)


def generate_random_tree(filename, num_numbers):
    with open(filename, 'w') as file:
        random_numbers = [str(random.randint(1, 100)) for _ in range(num_numbers)]
        file.write(','.join(random_numbers))


def create_btree(numbers):
    if not numbers:
        return None

    rand = random.randint(0, len(numbers) - 1)
    node = TreeNode(numbers[rand])
    node.left = create_btree(numbers[:rand])
    node.right = create_btree(numbers[rand + 1:])
    return node


def pre_order(node):
    if node:
        print(node.value, '->', node.left.value if node.left else None, node.right.value if node.right else None)
        pre_order(node.left)
        pre_order(node.right)


def tree_to_dict(node):
    if node is None:
        return None
    return {
        'value': node.value,
        'left': tree_to_dict(node.left),
        'right': tree_to_dict(node.right)
    }


def save_tree_to_json(node, filename):
    tree_dict = tree_to_dict(node)
    with open(filename, 'w') as file:
        json.dump(tree_dict, file, indent=4)


def load_tree_from_json(filename):
    with open(filename, 'r') as file:
        tree_dict = json.load(file)
    return dict_to_tree(tree_dict)


def dict_to_tree(data):
    if data is None:
        return None
    node = TreeNode(data['value'])
    node.left = dict_to_tree(data['left'])
    node.right = dict_to_tree(data['right'])
    return node


if __name__ == '__main__':
    file_name = 'tree.txt'
    number = 100000
    generate_random_tree(file_name, number)
    with open(file_name, 'r') as file:
        data = [int(i) if i else None for i in file.read().split(',')]
    root = create_btree(data)
    #pre_order(root)

    # Сохранение дерева в JSON файл
    json_filename = 'tree.json'
    save_tree_to_json(root, json_filename)
    print(f"Дерево сохранено в {json_filename}")

    # Загрузка дерева из JSON файла
    root_from_json = load_tree_from_json(json_filename)

    # Вывод дерева из JSON файла
    print("\nДерево, загруженное из JSON файла:")
    pre_order(root_from_json)
    target_leaves = int(input("Введите кол-во листьев: "))
    if number % 2:
        number /= 2 + 1
    else:
        number /= 2

    total_start_time = time.time()
    subtrees, _ = find_subtrees_with_leaves(root_from_json, target_leaves)
    total_end_time = time.time()
    total_elapsed_time = total_end_time - total_start_time

    if subtrees:
        for subtree in subtrees:
            print(f"Найдено поддерево с {target_leaves} листьями:")
            print(f"Корень: {subtree[0].value}, Глубина: {subtree[2]}")
            if subtree[0].left:
                print("Левое поддерево:", subtree[0].left.value)
            if subtree[0].right:
                print("Правое поддерево:", subtree[0].right.value)
            print()
    else:
        print(f"Поддерева с {target_leaves} не найдено")
    print(f"Общее время выполнения поиска всех поддеревьев: {total_elapsed_time:.6f} секунд")
