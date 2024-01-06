---
title: TailwindCSS Overview.
url: https://www.yuque.com/stevenyin/liv/qzlely81v31ab9o4
---

<a name="cv0ni"></a>

## What is TailwindCSS

TailwindCSS is a utility-first CSS framework that provides a set of pre-defined CSS classes that can be used to quickly style HTML elements. It is designed to make it easier to build responsive, customizable, and scalable user interfaces for web applications. Unlike traditional CSS frameworks that provide pre-built components and templates, TailwindCSS focuses on providing a low-level set of building blocks that can be combined to create custom designs.
With TailwindCSS, you can apply styles to HTML elements by adding pre-defined classes to your HTML markup. These classes are organized into categories such as layout, typography, colors, and more, making it easy to apply styles to specific parts of your interface. TailwindCSS also includes responsive design utilities that allow you to apply different styles based on the screen size, as well as a comprehensive set of utility classes for spacing, sizing, and positioning.
One of the benefits of using TailwindCSS is that it can help reduce the amount of custom CSS you need to write. By using pre-defined classes for common styles, you can write less CSS code and focus more on building your application. Additionally, because TailwindCSS provides a consistent set of styles, it can help ensure that your interface is visually consistent and easier to maintain over time. <a name="OrvLM"></a>

## Please give me some classic css code and TailwindCSS code to show the differences

Sure, here's an example of classic CSS code and its equivalent in TailwindCSS:
Classic CSS Code:

```css
.btn {
  display: inline-block;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 600;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
  border: 2px solid #000;
  border-radius: 4px;
  background-color: #fff;
  color: #000;
}

.btn:hover {
  background-color: #000;
  color: #fff;
}

```

TailwindCSS Code:

```html
<button class="inline-block px-6 py-3 font-semibold text-center whitespace-nowrap align-middle border-2 border-black rounded bg-white text-black hover:bg-black hover:text-white">
  Click Me
</button>

```

As you can see, the classic CSS code applies styles using properties such as `padding`, `font-size`, `background-color`, and `color`. In contrast, the `TailwindCSS` code applies styles using classes such as `px-6`, `py-3`, `font-semibold,` and `bg-white`. The `TailwindCSS` classes are designed to be composable, meaning you can combine multiple classes to create more complex styles.
In addition, the `TailwindCSS` code uses the hover variant to apply styles on hover, which is a built-in feature of the framework. Overall, TailwindCSS aims to make it easier and faster to write CSS by providing a more declarative syntax and a comprehensive set of utility classes.

<a name="fiOr6"></a>

## How to combine TailwindCSS with React.js?

Combining TailwindCSS with React.js is a relatively simple process. Here are the steps you can follow:

1. Install TailwindCSS: You can install TailwindCSS by running the following command in your terminal:

```shell
npm install tailwindcss
```

2. Configure TailwindCSS: Create a `tailwind.config.js` file in the root of your project and add the following code:

```javascript
module.exports = {
  mode: 'jit',
  purge: [
    './src/**/*.js',
    './src/**/*.jsx',
    './src/**/*.ts',
    './src/**/*.tsx',
  ],
  theme: {},
  variants: {},
  plugins: [],
}

```

This config file sets up TailwindCSS to work with your React project and configures the framework to remove unused styles in production builds.

3. Import TailwindCSS: Next, you need to import TailwindCSS into your project. You can do this by adding the following line to your `index.js` or `index.tsx` file:

```javascript
import './index.css';
```

4. Create a CSS file: Create a new file in your project called `index.css`. In this file, you can write your custom styles and also include the TailwindCSS classes you want to use. For example, you could write:

```css
.button {
  @apply inline-block px-4 py-2 font-semibold text-white bg-blue-500 rounded;
}

```

This code defines a custom .button class that uses TailwindCSS classes to style a button with a blue background and white text.

5. Use TailwindCSS classes in your components:

Finally, you can use the TailwindCSS classes you defined in your CSS file in your React components. For example:

```jsx
import React from 'react';
import './index.css';

function App() {
  return (
    <div>
      <button className="button">Click Me</button>
    </div>
  );
}

export default App;

```

That's it! You can now use TailwindCSS classes to style your React components. Note that you can also use the `@apply` directive to apply multiple TailwindCSS classes in your custom CSS, which can make it easier to create more complex styles.
