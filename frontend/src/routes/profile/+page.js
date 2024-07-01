export async function load ({ fetch }) {
    const response = await fetch ("http://localhost:8000/users");
    const users = await response.json();
    const title = "hiiiiiiiii";
    return { users };
}