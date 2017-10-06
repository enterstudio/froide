<template>
  <div class="card">
    <div class="card-body">
      <div class="form-group row">
        <div class="col" :class="{ 'text-danger': errors.first_name }">
          <label class="control-label" for="id_first_name" :class="{ 'text-danger': errors.first_name }">
            {{ i18n.yourFirstName }}
          </label>
          <input v-model="first_name" type="text" name="first_name" class="form-control" :class="{ 'is-invalid': errors.first_name }" id="id_first_name" :placeholder="form.first_name.placeholder"/>
          <p v-for="e in errors.first_name">{{ e.message }}</p>
          <small v-if="form.first_name.help_text">{{ form.first_name.help_text }}</small>
        </div>
        <div class="col" :class="{ 'text-danger': errors.last_name }">
          <label class="control-label" for="id_last_name" :class="{ 'text-danger': errors.last_name }">
            {{ i18n.yourFirstName }}
          </label>
          <input v-model="last_name" type="text" name="last_name" class="form-control" :class="{ 'is-invalid': errors.last_name }" id="id_last_name" :placeholder="form.last_name.placeholder"/>
          <p v-for="e in errors.last_name">{{ e.message }}</p>
          <small v-if="form.last_name.help_text">{{ form.last_name.help_text }}</small>
        </div>
      </div>

      <div class="form-group row">
        <label for="id_user_email" class="col-sm-3 col-form-label" :class="{ 'text-danger': errors.user_email }">
          {{ i18n.yourEmail }}
        </label>
        <div class="col-sm-9">
          <p v-if="user.id" id="email_address" class="form-control">
            {{ user.email }}
          </p>
          <div v-else>
            <input v-model="email" type="email" name="user_email" class="form-control" :class="{ 'is-invalid': errors.user_email }" :placeholder="form.user_email.placeholder"/>
            <p v-for="e in errors.user_email" class="text-danger">{{ e.message }}</p>
          </div>
        </div>
      </div>

      <div class="form-group row">
        <label for="id_address" class="col-sm-3 col-form-label" :class="{ 'text-danger': errors.address }">
          {{ i18n.yourAddress }}
        </label>
        <div class="col-sm-9">
          <p v-if="user.id" id="email_address" class="form-control">
            {{ user.email }}
          </p>
          <div v-else>
            <textarea v-model="address" name="address" class="form-control" :class="{ 'is-invalid': errors.address }" :placeholder="form.address.placeholder"></textarea>
            <p v-for="e in errors.address">{{ e.message }}</p>
            <p class="help-block">{{ form.address.help_text }}</p>
          </div>
        </div>
      </div>

      <div v-if="config.settings.user_can_hide_web">
        <div class="checkbox">
          <label>
            <input v-model="private" type="checkbox" name="private" />
            {{ form.private.label }}
          </label>
          <p class="help-block">
            {{ form.private.help_text }}
          </p>
        </div>
      </div>

    </div>
  </div>
</template>

<script>

import {mapGetters, mapMutations} from 'vuex'

import {
  UPDATE_FIRST_NAME, UPDATE_LAST_NAME, UPDATE_EMAIL, UPDATE_ADDRESS,
  UPDATE_PRIVATE
} from '../store/mutation_types'

export default {
  name: 'user-registration',
  props: [
    'config', 'formJson'
  ],
  created () {
    if (this.form.first_name.value !== null) {
      this.updateFirstName(this.form.first_name.value)
    }
    if (this.form.last_name.value !== null) {
      this.updateLastName(this.form.last_name.value)
    }
    if (this.form.user_email.value !== null) {
      this.updateEmail(this.form.user_email.value)
    }
    if (this.form.address.value !== null) {
      this.updateAddress(this.form.address.value)
    }
    if (this.form.private.value !== null) {
      this.updatePrivate(this.form.private.value)
    }
  },
  computed: {
    _form () {
      return JSON.parse(this.formJson)
    },
    form () {
      return this._form.fields
    },
    errors () {
      return this._form.errors
    },
    i18n () {
      return this.config.i18n
    },
    first_name: {
      get () {
        return this.$store.state.user.first_name
      },
      set (value) {
        this.updateFirstName(value)
      }
    },
    last_name: {
      get () {
        return this.$store.state.user.last_name
      },
      set (value) {
        this.updateLastName(value)
      }
    },
    email: {
      get () {
        return this.$store.state.user.email
      },
      set (value) {
        this.updateEmail(value)
      }
    },
    address: {
      get () {
        return this.$store.state.user.address
      },
      set (value) {
        this.updateAddress(value)
      }
    },
    private: {
      get () {
        return this.$store.state.user.private
      },
      set (value) {
        this.updatePrivate(value)
      }
    },
    ...mapGetters([
      'user'
    ])
  },
  methods: {
    ...mapMutations({
      updateFirstName: UPDATE_FIRST_NAME,
      updateLastName: UPDATE_LAST_NAME,
      updateAddress: UPDATE_ADDRESS,
      updateEmail: UPDATE_EMAIL,
      updatePrivate: UPDATE_PRIVATE
    })
  }
}
</script>