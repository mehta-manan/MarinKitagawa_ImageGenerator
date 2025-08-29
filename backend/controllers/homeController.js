const sayHello = async (req, res) => {
  res
    .status(200)
    .json({ status: 200, message: "Hello from Marin Kitagawa Image Generator Server!" });
};

exports.sayHello = sayHello;
