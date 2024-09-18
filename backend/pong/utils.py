def lerp(first, second, inter, dt):
	diff = second - first
	return (first + (diff * inter * dt))