const API_DJANGO = "http://127.0.0.1:8000";
const API_FASTAPI = "http://127.0.0.1:8001";

let selectedSeats = [];

function login() {
  fetch("http://127.0.0.1:8000/api/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      email: document.getElementById("email").value,
      password: document.getElementById("password").value
    })
  })
  .then(response => {
    if (!response.ok) {
      return response.text().then(text => {
        throw new Error(text);
      });
    }
    return response.json();
  })
  .then(data => {
    console.log("LOGIN SUCCESS:", data);
    localStorage.setItem("token", data.access);
    window.location.href = "seats.html";
  })
  .catch(err => {
    console.error("LOGIN ERROR:", err);
    alert("Login failed — check console");
  });
}

function renderSeats() {
  fetch(`http://127.0.0.1:8001/seats/list?show_id=1`)
    .then(res => res.json())
    .then(seats => {
      const container = document.getElementById("seats");
      container.innerHTML = "";

      seats.forEach(seat => {
        const div = document.createElement("div");
        div.innerText = seat.seat_id;
        div.classList.add("seat");

        if (seat.status === "AVAILABLE") {
          div.onclick = () => toggleSeat(div, seat.seat_id);
        }

        if (seat.status === "LOCKED") {
          div.classList.add("locked");
        }

        if (seat.status === "BOOKED") {
          div.classList.add("booked");
        }

        container.appendChild(div);
      });
    });
}


function toggleSeat(div, seat) {
  if (div.classList.contains("locked") || div.classList.contains("booked")) {
    return;
  }

  if (selectedSeats.includes(seat)) {
    selectedSeats = selectedSeats.filter(s => s !== seat);
    div.classList.remove("selected");
  } else {
    selectedSeats.push(seat);
    div.classList.add("selected");
  }
}


function lockSeats() {
  console.log("Selected seats:", selectedSeats);

  fetch("http://127.0.0.1:8001/seats/lock", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + localStorage.getItem("token")
    },
    body: JSON.stringify({
      show_id: 1,
      seats: selectedSeats
    })
  })
  .then(res => {
    console.log("Response status:", res.status);
    return res.json();
  })
  .then(data => {
    console.log("LOCK RESPONSE:", data);
    alert(JSON.stringify(data));
  })
  .catch(err => {
    console.error("LOCK ERROR:", err);
  });
}


function payNow() {
  console.log("Pay clicked");

  fetch("http://127.0.0.1:8001/payment/create-order", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + localStorage.getItem("token")
    },
    body: JSON.stringify({ amount: 3 })
  })
  .then(async res => {
    const data = await res.json();
    if (!res.ok) throw data;
    return data;
  })
  .then(order => {
    console.log("Order created:", order);

    if (!window.Razorpay) {
      alert("Razorpay SDK not loaded");
      return;
    }

    const options = {
      key: order.key,
      amount: order.amount,
      currency: "INR",
      name: "Movie Booking",
      description: "Seat Booking",
      order_id: order.order_id,

      handler: function (response) {
        verifyPayment(response);
      },

      theme: { color: "#3399cc" }
    };

    const rzp = new Razorpay(options);
    rzp.open();
  })
  .catch(err => {
    console.error("Payment error:", err);
    alert("Payment failed — check console");
  });
}


function openRazorpay(order) {
  var options = {
    key: order.key,
    amount: order.amount,
    currency: "INR",
    name: "Movie Booking",
    description: "Seat Booking",
    order_id: order.order_id,

    handler: function (response) {
      verifyPayment(response);
    },

    theme: {
      color: "#3399cc"
    }
  };

  var rzp = new Razorpay(options);
  rzp.open();
}





function verifyPayment(response) {
  fetch("http://127.0.0.1:8001/payment/verify", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + localStorage.getItem("token")
    },
    body: JSON.stringify({
      razorpay_order_id: response.razorpay_order_id,
      razorpay_payment_id: response.razorpay_payment_id,
      razorpay_signature: response.razorpay_signature,
      seats: selectedSeats
    })
  })
  .then(res => res.json())
  .then(data => {
    alert(" Booking confirmed! Booking ID: " + data.booking_id);
    selectedSeats = [];
    renderSeats();
  })
  .catch(err => {
    console.error(err);
    alert("Payment verification failed");
  });
}

function cancelBooking(bookingId) {
  fetch("http://127.0.0.1:8001/payment/cancel", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + localStorage.getItem("token")
    },
    body: JSON.stringify({ booking_id: bookingId })
  })
  .then(res => res.json())
  .then(data => alert(data.message))
  .catch(err => console.error(err));
}
