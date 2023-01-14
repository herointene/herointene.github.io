---
tags:
- vue
- javascript
- tutorial
---
## Paginated data in Vue:

Here is an example of how you can display paginated data in a table using Vue.js:

```javascript
<template>
  <div>
    <table>
      <thead>
        <tr>
          <th>Column 1</th>
          <th>Column 2</th>
          <th>Column 3</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in displayedData" :key="row.id">
          <td>{{ row.col1 }}</td>
          <td>{{ row.col2 }}</td>
          <td>{{ row.col3 }}</td>
        </tr>
      </tbody>
    </table>
    <button @click="previousPage">Previous</button>
    <button @click="nextPage">Next</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      data: [],  // this is the array of all rows
      pageSize: 100,  // number of rows to display per page
      currentPage: 1  // the current page being displayed
    }
  },
  computed: {
    displayedData() {
      // slice the array to get the rows for the current page
      const start = (this.currentPage - 1) * this.pageSize
      return this.data.slice(start, start + this.pageSize)
    }
  },
  methods: {
    previousPage() {
      if (this.currentPage > 1) {
        this.currentPage--
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++
      }
    }
  }
}
</script>
```
This code uses a computed property `displayedData` to slice the `data` array and return only the rows that should be displayed on the current page. The `previousPage` and `nextPage` methods are used to update the `currentPage` variable, which determines which slice of the `data` array is displayed.

You can also add a label or input field to display the current page and allow the user to jump to a specific page. You can also add buttons or links to go directly to the first or last page.

## After discussion, the full version with composition API:

```javascript
<template>
  <div>
    <table>
      <!-- table contents -->
    </table>
    <button @click="previousPage" :disabled="currentPage === 1">Previous</button>
    <button v-for="page in pageRange" :key="page" @click="goToPage(page)" :class="{ active: currentPage === page }">{{ page }}</button>
    <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    <label for="page-size">Rows per page:</label>
    <select id="page-size" v-model="pageSize">
      <option value="25">25</option>
      <option value="50">50</option>
      <option value="100">100</option>
      <option value="200">200</option>
    </select>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  setup() {
    const data = ref([])
    const pageSize = ref(100)
    const currentPage = ref(1)

    function previousPage() {
      if (currentPage.value > 1) {
        currentPage.value--
      }
    }

    function nextPage() {
      if (currentPage.value < totalPages.value) {
        currentPage.value++
      }
    }

    function goToPage(page) {
      currentPage.value = page
    }

    const displayedData = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value
      return data.value.slice(start, start + pageSize.value)
    })

    const totalPages = computed(() => Math.ceil(data.value.length / pageSize.value))

    const pageRange = computed(() => Array.from({ length: totalPages.value }, (v, k) => k + 1))

    return {
      data,
      pageSize,
      currentPage,
      displayedData,
      totalPages,
      pageRange,
      previousPage,
      nextPage,
      goToPage
    }
  }
}
</script>

```

## About pageRange, Array.from() explaination:

`Array.from` is a method in JavaScript that creates a new, shallow-copied Array instance from an array-like or iterable object.

The syntax for `Array.from` is:

```javascript
Array.from(arrayLike, mapFn, thisArg)

```

The first argument, `arrayLike`, is the object to be converted to an array. The second argument, `mapFn`, is an optional callback function that is called for each element in the array. The third argument, `thisArg`, is an optional value to use as `this` when executing `mapFn`.

In the code you provided, `Array.from` is being used with an object with a `length` property set to `this.totalPages`, and a callback function that returns the index of the element plus 1.

Here is how this code can be explained:

-   The object `{ length: this.totalPages }` creates an object with a single property, `length`, set to the value of `this.totalPages`.
-   The callback function `(v, k) => k + 1` is called for each element in the array. The arguments `v` and `k` represent the value and index of the element, respectively. The function returns the index plus 1.
-   The resulting array will have a length equal to `this.totalPages`, and will contain the elements `1`, `2`, `3`, etc., up to the value of `this.totalPages`.

For example, if `this.totalPages` is 5, the resulting array will be `[1, 2, 3, 4, 5]`.

This array can then be used in a `v-for` directive to generate buttons for each page.

See the MDN guide: [link](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from)
