# Adding a Favicon to the Web Interface

To add a favicon to the web interface, follow these steps:

1. Create a favicon.ico file (you can use online tools like favicon.io to convert an image to favicon format)
2. Place the favicon.ico file in this directory (static/images/)
3. Add the following line to the <head> section of templates/index.html:

```html
<link rel="icon" href="{{ url_for('static', filename='images/favicon.ico') }}">
```

This will make the favicon appear in the browser tab when users visit your web interface.

# Adding Other Images

You can also add other images to this directory and use them in your web interface.
For example, you could add a logo to the header of the web interface by:

1. Adding the logo image file to this directory (e.g., logo.png)
2. Adding the following HTML to templates/index.html:

```html
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo" class="logo">
```

3. Adding appropriate CSS styles to static/style.css:

```css
.logo {
  max-height: 50px;
  margin-right: 20px;
}
