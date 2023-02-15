<template>
    <div class="app">
      <div class="items">
        <div v-for="note in notes">
            <div class="content">
                <input type="checkbox" v-model="note.isChecked" @click="change_checkbox_value(note.id)"/>
                {{note.content}}
            </div>
            <div class="methods">
                <button @click="choice_updated_note(note.id)">Edit</button>
                <button @click="delete_note(note.id)">Delete</button>
            </div>
        </div>
      </div>
      <div>
        <input type="text" v-model="main_input_content"/>
        <button @click="create_update_note">OK</button>
        <button @click="cancel">Cancel</button>
      </div>
    </div>
</template>

<script setup>
  import { ref } from 'vue'
  import { onMounted } from 'vue'

  let notes = ref([])
  let main_input_content = ref("")
  let updated_note_id = 0

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
    let current_note_num

    for(let i = 0; i < notes.value.length; i++) {
      if (notes.value[i]['id'] == note_id) {
        current_note_num = i
        break
      }
    }
    notes.value.splice(current_note_num, 1)

    cancel()

  }
  async function create_update_note() {
    if (updated_note_id == 0) {
      let resp = await fetch("http://127.0.0.1:8000/items/create", {
        method: 'POST',
        headers:
        {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "content": main_input_content.value
        })
      })

    let result = await resp.json()
    notes.value.push(result)

    }
    else {
        let note_is_checked
        let current_note_num

        for(let i = 0; i < notes.value.length; i++) {
          if (notes.value[i]['id'] == updated_note_id) {
            note_is_checked = notes.value[i]['isChecked']
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
            "content": main_input_content.value,
            "isChecked": note_is_checked
          })
        })
        let result = await resp.json()
        notes.value[current_note_num] = result

    }
    cancel()
  }

  function cancel() {
    updated_note_id = 0
    main_input_content.value = ''
  }

  function choice_updated_note(note_id) {
    let note_content

    for(let i = 0; i < notes.value.length; i++) {
      if (notes.value[i].id == note_id) {
        note_content = notes.value[i].content
        break
      }
    }

    updated_note_id = note_id
    main_input_content.value = note_content
  }

  async function change_checkbox_value(note_id) {
      let note_is_checked
      let note_content
      let current_note_num

      for(let i = 0; i < notes.value.length; i++) {
        if (notes.value[i]['id'] == note_id) {
          note_is_checked = notes.value[i]['isChecked']
          note_content = notes.value[i]['content']
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
        "id": note_id,
        "content": note_content,
        "isChecked": !(note_is_checked)
      })
    })
    let result = await resp.json()
  }

  onMounted(async () => {
    let resp = await fetch("http://127.0.0.1:8000/items", {method: 'GET'})
    let list = await resp.json()
    for (var id in list){
        notes.value.push(list[id])
    }
})

</script>

<style>
</style>
