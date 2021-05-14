_layout = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6"
      crossorigin="anonymous"
    />
    <title>{{ title }}</title>
  </head>
  <body>
      <div class="container p-2">
    <div class="row d-block">
      {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
      {% for category, message in messages %}
      <div class=" text-center alert alert-{{ category }}">
        {{ message }}
      </div>
    </div>
  </div>
  {% endfor %}
  {% endif %}
  {% endwith %}
  </div>
      <div class="main">
            {% block main %} {% endblock main %}
    </div>
    <script
      src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.1/dist/umd/popper.min.js"
      integrity="sha384-SR1sx49pcuLnqZUnnPwx6FCym0wLsk5JZuNx2bPPENzswTNFaQU1RDvt3wT4gWFG"
      crossorigin="anonymous"
    ></script>
    <script
      src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.min.js"
      integrity="sha384-j0CNLUeiqtyaRmlzUHCPZ+Gy5fQu0dQ6eZ/xAww941Ai1SxSY+0EQqNXNE6DZiVc"
      crossorigin="anonymous"
    ></script>
  </body>
</html>
"""

_login = """
{% extends 'layout.html' %} {% block main %}
<style>
  .log-form {
    width: 350px;
  }
</style>
<div class="container my-5">
  <div class="row">
    <div class="col-md" style="display: block; text-align: center">
      <form method="POST" action="/auth/login" class="log-form shadow p-3 mb-5 bg-body rounded" style="
          display: inline-block;
          margin-left: auto;
          margin-right: auto;
          text-align: left;
        ">
        <h2 class="text-center mb-2">{{ cfg['LOGIN_PAGE_TITLE'] }}</h2>
        <div class="mb-3">
          <label for="username_field" class="form-label">{{ cfg['LOGIN_LABEL_USERNAME'] }}</label>
          <input name="username" type="text" class="form-control" id="username_field" required />
        </div>
        <div class="mb-3">
          <label for="password_field" class="form-label">{{ cfg['LOGIN_LABEL_PASSWORD'] }}</label>
          <input name="password" type="password" class="form-control" id="password_field" required />
        </div>
        <div class="d-grid gap-2 mb-2">
          <button class="btn {{ cfg['LOGIN_BTN'] }}" type="submit">{{ cfg['LOGIN_BTN_TEXT'] }}</button>
        </div>
        <p class="text-muted text-center">
          Or <a style="text-decoration: none" href="{{ reg }}">Register</a>
        </p>
      </form>
    </div>
  </div>
</div>
{% endblock main %}
"""

_register = """
{% extends 'layout.html' %} {% block main %}
<style>
  .reg-form {
    width: 350px;
  }
</style>
<div class="container my-5">
  <div class="row">
    <div class="col-md" style="display: block; text-align: center">
      <form method="POST" action="/auth/register" class="reg-form shadow p-3 mb-5 bg-body rounded" style="
          display: inline-block;
          margin-left: auto;
          margin-right: auto;
          text-align: left;
        ">
        <h2 class="text-center mb-2">{{ cfg['REGISTER_PAGE_TITLE'] }}</h2>
        <div class="mb-3">
          <label for="email_field" class="form-label">{{ cfg['REGISTER_LABEL_EMAIL'] }}</label>
          <input type="email" class="form-control" id="email_field" aria-describedby="emailHelp" name="email" />
        </div>
        <div class="mb-3">
          <label for="username_field" class="form-label">{{ cfg['REGISTER_LABEL_USERNAME'] }}</label>
          <input min="3" type="text" class="form-control" id="username_field" name="username" required />
        </div>
        <div class="mb-3">
          <label for="password_field" class="form-label">{{ cfg['REGISTER_LABEL_PASSWORD'] }}</label>
          <input min="7" max="64" type="password" class="form-control" id="password_field" name="password" required />
          <span id="error_msg" class="text-danger mt-2" style="padding: 5px">
          </span>
        </div>
        <div class="d-grid gap-2 mb-2">
          <button class="btn {{ cfg['REGISTER_BTN'] }}" type="submit" id="form_btn">
            {{ cfg['REGISTER_BTN_TEXT'] }}
          </button>
        </div>
        <p class="text-muted text-center">
          Or <a style="text-decoration: none" href="{{ log }}">Login</a>
        </p>
      </form>
    </div>
  </div>
</div>
<script src="https://code.jquery.com/jquery-3.6.0.slim.js"
  integrity="sha256-HwWONEZrpuoh951cQD1ov2HUK5zA5DwJ1DNUXaM6FsY=" crossorigin="anonymous"></script>
<script>
  $("#form_btn").attr("disabled", true);
  $("#password_field").on("change", function () {
    if (this.value.length < 8) {
      $("#form_btn").attr("disabled", true);
      $("#error_msg").html("Password must be 8 characters long!");
      $(this).focus();
      return false;
    } else {
      $("#error_msg").html("");
      $("#form_btn").removeAttr("disabled");
    }
  });
</script>
{% endblock main %}
""" 