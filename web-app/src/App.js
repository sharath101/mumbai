import './App.css';
import Login from './components/login'

function App() {

  return (
    <header id="header" className="fixed-top ">
    <div className="container-fluid d-flex align-items-center justify-content-lg-between">
        <div class="row">
            <div class="col-md-3 align-center">
      <h1 className="logo me-auto me-lg-0"><a href="index.html">Gp<span>.</span></a></h1>
                </div>
      {/* <!-- Uncomment below if you prefer to use an image logo -->
      <!-- <a href="index.html" class="logo me-auto me-lg-0"><img src="assets/img/logo.png" alt="" class="img-fluid"></a>--> */}
        <div class="col-md-6">
      <nav id="navbar" className="navbar order-last order-lg-0">
        <ul>
          <li><a class="nav-link scrollto active" href="#hero">Home</a></li>
          <li><a class="nav-link scrollto" href="#about">About</a></li>
          <li><a class="nav-link scrollto" href="#tournaments">Tournaments</a></li>
          <li><a class="nav-link scrollto " href="#leaderboard">Leaderboard</a></li>
          <li><a class="nav-link scrollto" href="#contact">Contact</a></li>
        </ul>
        <i className="bi bi-list mobile-nav-toggle"></i>
      </nav>
            </div>
        <div class="col-md-3">
      <Login/>
            </div>
        </div>
    </div>
  </header>
  );
}

export default App;
