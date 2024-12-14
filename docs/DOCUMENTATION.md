[<mark style="font-size:20px; background-color: grey">OVERVIEW</mark>](../README.md) |
[<mark style="font-size:20px; background-color: grey">GETTING STARTED</mark>](GETTINGSTARTED.md) |
[<mark style="font-size:20px; background-color: grey">NEW SERVICES</mark>](NEWSERVICES.md) |
[<mark style="font-size:20px; background-color: lightblue">DOCUMENTATION</mark>](DOCUMENTATION.md) |
[<mark style="font-size:20px; background-color: grey">PROFILERS</mark>](PROFILERS.md)

# Documentation
The package also has an NGINX container to host interactive documentation.
Calling the following commands from the package root directory will result in
a local web browser displaying the package HTML documentation.

## Build Documentation
```bash
make docs
```

## View Documentation without Building
```bash
make docs-view
```

## Documentation are viewable at the following urls:
Many browsers often convert HTTP to HTTPS so manually typing in the url is 
sometimes required.
```bash
http://localhost:<PORT_NGINX>/api_gateway/
http://localhost:<PORT_NGINX>/front_end/
http://localhost:<PORT_NGINX>/model_serving/
```

<br>

[<mark style="font-size:20px; background-color: grey">OVERVIEW</mark>](../README.md) |
[<mark style="font-size:20px; background-color: grey">GETTING STARTED</mark>](GETTINGSTARTED.md) |
[<mark style="font-size:20px; background-color: grey">NEW SERVICES</mark>](NEWSERVICES.md) |
[<mark style="font-size:20px; background-color: lightblue">DOCUMENTATION</mark>](DOCUMENTATION.md) |
[<mark style="font-size:20px; background-color: grey">PROFILERS</mark>](PROFILERS.md)
