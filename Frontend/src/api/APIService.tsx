//@ts-nocheck
const url =
  import.meta.env.MODE === "development"
    ? "http://localhost:5000"
    : import.meta.env.VITE_BACKEND_API_BASE_URL;

export default class APIService {
  static async PostData(body: any, route: string) {
    try {
      Response = await fetch(url.concat(route), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Accept: "application/json",
        },
        body: JSON.stringify(body),
      }).then(async (res) => {
        return res;
      });
      return await Response.json();
    } catch (error) {
      return console.log(error);
    }
  }
  static async GetData(route: string) {
    try {
      Response = await fetch(url.concat(route), {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Accept: "application/json",
        },
      }).then(async (res) => {
        return res;
      });
      return await Response.json();
    } catch (error) {
      return console.log(error);
    }
  }
}