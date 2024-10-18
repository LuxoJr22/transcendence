export function lerp(current : number, target : number, add : number)
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
export function random(min : number, max : number)
{
	return (Math.random() * (max - min)) + min;
}

export function equal(value : number, comp : number)
{
	if (value >= comp - 0.01 && value <= comp + 0.01 )
		return (1);
	return (0);
}