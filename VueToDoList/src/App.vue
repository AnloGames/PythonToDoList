<template>
    <div class="app">
      <div id="items" class="items">
        <div id="item" v-for="note in Notes">
            {{note}}
        </div>
      </div>
      <div id="methods">
        <input type="text" id="noteContent"/>
      </div>
    </div>
</template>

<script setup>
  import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.7.8/dist/vue.esm.browser.js'
  import { onMounted } from 'vue'

  let notes
  let updated_note_id = 0

  async function load_notes() {
    let resp = await fetch("http://127.0.0.1:8000/items", {method: 'GET'})
    notes = await resp.json()
  }

  async function delete_note(note_id) {
    let resp = await fetch("http://127.0.0.1:8000/items/delete", {
      method: 'POST',
      headers:
      {
         "Content-Type": "application/json"
      },
      body: JSON.stringify({
        "id": note_id
      })
    })
    let result = await resp
    let note_list = document.getElementById('items')
    note_list.innerHTML = ''

    cancel()
    load_notes()

  }
  async function create_update_note() {
    let content_input = document.getElementById("noteContent")
    let content = content_input.value

    if (updated_note_id == 0) {
      let resp = await fetch("http://127.0.0.1:8000/items/create", {
        method: 'POST',
        headers:
        {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "content": content
        })
      })

    let result = await resp
    let note_list = document.getElementById('items')
    note_list.innerHTML = ''

    load_notes()
    }


    else {
        let note_is_checked
        let current_note_num

        for(let i = 0; i < notes.length; i++) {
          if (notes[i]['id'] == updated_note_id) {
            note_is_checked = notes[i]['isChecked']
            current_note_num = i
            break
          }
        }

        let resp = await fetch("http://127.0.0.1:8000/items/update", {
          method: 'POST',
          headers:
          {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            "id": updated_note_id,
            "content": content,
            "isChecked": note_is_checked
          })
        })
        let result = await resp.json()
        let note_list = document.getElementById('items')
        note_list.innerHTML = ''

        load_notes()
    }
    cancel()
  }

  function cancel() {
    let content_input = document.getElementById("noteContent")
    content_input.value = ''
    updated_note_id = 0
  }

  function choice_updated_note(note_id) {
    updated_note_id = note_id
    let note_content

    for(let i = 0; i < notes.length; i++) {
      if (notes[i]['id'] == updated_note_id) {
        note_content = notes[i]['content']
        break
      }
    }

    let content_input = document.getElementById("noteContent")
    content_input.value = note_content
  }

  async function change_checkbox_value(note_id) {
      let note_is_checked
      let note_content

      for(let i = 0; i < notes.length; i++) {
        if (notes[i]['id'] == note_id) {
          note_is_checked = notes[i]['isChecked']
          note_content = notes[i]['content']
          break
        }
      }

      let resp = await fetch("http://127.0.0.1:8000/items/update", {
      method: 'POST',
      headers:
      {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        "id": note_id,
        "content": note_content,
        "isChecked": !(note_is_checked)
      })
    })
    let result = await resp.json()
  }

  onMounted(async () => {
    var note_list = new Vue({
    el: '#item',
    data: {
        Notes: notes
    }
  })
  let ok_btn = document.createElement('button')
  ok_btn.textContent = "OK"
  ok_btn.onclick = () => create_update_note()

  let cancel_btn = document.createElement('button')
  cancel_btn.textContent = "Cancel"
  cancel_btn.onclick = () => cancel()

  let methods_div = document.getElementById("methods")
  methods_div.appendChild(ok_btn)
  methods_div.appendChild(cancel_btn)

  load_notes()
})

</script>

<style>
</style>
