import LoginPanel from "./components/Login/Login"
import Register from "./components/Register/Register"
import Dealers from "./components/Dealers/Dealers"
import Dealer from "./components/Dealers/Dealer"
import PostReview from "./components/Dealers/PostReview"
import Home from "./components/Home"
import About from "./components/About"
import Contact from "./components/Contact"
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/dealer/:id" element={<Dealer />} />
      <Route path="/postreview/:id" element={<PostReview />} />
    </Routes>
  );
}
export default App;
