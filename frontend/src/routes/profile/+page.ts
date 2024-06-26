export const load = async (loadEvent) => {
    const { fetch } = loadEvent
    const response = await fetch ("http://localhost:8000/users");
    const users = await response.json();
    return {
        users
    };
};