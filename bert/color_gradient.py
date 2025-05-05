def generate_gradients():
    steps = []
    n=500
    min_val = -100
    max_val = 100
    range_size = (max_val - min_val) / (n - 1) if n > 1 else 0

    for i in range(n - 1):
        start = min_val + i * range_size
        end = start + range_size
        ratio = (start + 100) / 200
        r = int(255 * (1 - ratio))
        g = int(255 * ratio)
        b = 0
        color = f"rgb({r},{g},{b})"
        steps.append({'range': [start, end], 'color': color})

    return steps