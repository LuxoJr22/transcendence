export function equal(value, comp)
{
	if (value >= comp - 0.01 && value <= comp + 0.01 )
		return (1);
	return (0);
}