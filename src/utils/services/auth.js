import axios from "axios";

const API_URL = "http://127.0.0.1:8000/users/";

const register = (user, avatar_url, mobile, special) => {
  return axios.post(API_URL + "users/", {

        "user": user,
        "avatar_url": avatar_url,
        "mobile_number": mobile,
        "special": special
                    
    
  });
};

const login = (username, password) => {
  return axios
    .post(API_URL + "signin", {
      username,
      password,
    })
    .then((response) => {
      if (response.data.accessToken) {
        localStorage.setItem("user", JSON.stringify(response.data));
      }

      return response.data;
    });
};

const logout = () => {
  localStorage.removeItem("user");
};

const getCurrentUser = () => {
  return JSON.parse(localStorage.getItem("user"));
};

const AuthService = {
  register,
  login,
  logout,
  getCurrentUser,
};

export default AuthService;
