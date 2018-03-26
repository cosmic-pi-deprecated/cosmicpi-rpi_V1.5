## Development
Make sure you have Node.js and npm installed on your computer. Run `npm run dev` to open application in a development mode. You can also specify different REST url by setting up an environment variable `API_URL`, eg. `API_URL=http://127.0.0.1:5000/api/ npm run dev`.

## Production
To compile the project and generate distribution files run `npm run build`.

## Guidelines
Vue.js is used as view library. Vuex is used for application state management which implements Redux architecture. Please read about [Redux architecture](https://vuex.vuejs.org/en/intro.html) before contributing to UI.