import Home from "./components/Home.vue";
import SignUp from "./components/SignUp.vue";
import { createRouter, createWebHistory } from "vue-router";
import Login from "./components/Login.vue";
import Add from "./components/Add.vue";
import Update from "./components/Update.vue";
import Search from "./components/Search.vue";
import Profile from "./components/Profile.vue";
import Following from "./components/Following.vue";
import Follower from "./components/Follower.vue";
import UserProfile from "./components/UserProfile.vue";

const routes = [
  {
    name: "Home",
    component: Home,
    path: "/",
  },
  {
    name: "SignUp",
    component: SignUp,
    path: "/sign-up",
  },
  {
    name: "Login",
    component: Login,
    path: "/login",
  },
  {
    name: "Add",
    component: Add,
    path: "/add",
  },
  {
    name: "Update",
    component: Update,
    path: "/update/:id",
  },
  {
    name: "Search",
    component: Search,
    path: "/search",
  },
  {
    name: "Profile",
    component: Profile,
    path: "/profile",
  },
  {
    name: "Following",
    component: Following,
    path: "/following",
  },
  {
    name: "Follower",
    component: Follower,
    path: "/follower",
  },
  {
    name: "UserProfile",
    component: UserProfile,
    path: "/userprofile/:id",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
