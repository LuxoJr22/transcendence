import * as THREE from 'three';

export function lerp(current, target, add)
{
	if (current < target && add > 0)
	{
		if (current + add < target)
			return (current + add);
		return (target);
	}
	else if (current > target && add < 0)
	{
		if (current + add > target)
			return (current + add);
		return (target);
	}
	return (current);
}
export function random(min, max)
{
	return (Math.random() * (max - min)) + min;
}

export function equal(value, comp)
{
	if (value >= comp - 0.01 && value <= comp + 0.01 )
		return (1);
	return (0);
}