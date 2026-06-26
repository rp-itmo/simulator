# Примеры использования симулятора

В данной папке находятся примеры запуска различных робототехнических систем и демонстрации возможностей симулятора.

## Базовые примеры

### TwoLink

```bash
uv run python examples/twolink_demo.py
```

Демонстрация работы двухзвенного манипулятора.

### Tree7

```bash
uv run python examples/tree7_demo.py
```

Запуск предопределённой древовидной робототехнической системы.

### Random Tree

```bash
uv run python examples/random_tree_demo.py
```

Генерация и запуск случайной древовидной структуры робота.

# Дополнительные примеры

## CartPole Balance

```bash
uv run python examples/cartpole_balance.py
```

Серия экспериментов с системой CartPole при различных начальных углах отклонения маятника. Позволяет сравнить влияние начального положения на поведение системы.

## Gravity Comparison

```bash
uv run python examples/gravity_comparison.py
```

Сравнение поведения одного и того же механизма при различных значениях ускорения свободного падения (Земля, Луна и Марс).

## Robot Tree Variants

```bash
uv run python examples/robot_tree_variants.py
```

Демонстрация влияния параметров генерации дерева (`bf`, `taper`, `skew`) на форму и структуру создаваемой робототехнической системы.
