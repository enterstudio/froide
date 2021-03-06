<template>
  <div class="make-request-container">
    <request-form-breadcrumbs
      :i18n="i18n"
      :multiRequest="multiRequest"
      :hasPublicBodies="hasPublicBodies"
      :hidePublicbodyChooser="hidePublicbodyChooser"></request-form-breadcrumbs>

    <div :class="{container: !multiRequest, 'container-multi': multiRequest}">

      <slot name="messages"></slot>

      <div class="row justify-content-lg-center">
        <div class="col-lg-12">

          <fieldset v-if="stepSelectPublicBody" id="step-publicbody" class="mt-5">
            <div v-if="multiRequest">
              <publicbody-multi-chooser
                name="publicbody"
                :defaultsearch="publicBodySearch"
                :scope="pbScope"
                :config="config">
                <template slot="publicbody-missing">
                  <slot name="publicbody-missing"></slot>
                </template>
              </publicbody-multi-chooser>
            </div>
            <div v-else>
              <div class="row">
                <div class="col-lg-7">
                  <slot name="publicbody-legend-title"></slot>
                  <slot name="publicbody-help-text"></slot>
                </div>
              </div>
              <div class="row">
                <div class="col-lg-8">
                  <publicbody-chooser
                    name="publicbody"
                    :defaultsearch="publicBodySearch"
                    :scope="pbScope"
                    :config="config"
                    :list-view="publicBodyListView"></publicbody-chooser>
                </div>
                <div class="col-lg-4 small">
                  <slot name="publicbody-missing"></slot>
                </div>
              </div>
            </div>
          </fieldset>

          <fieldset v-if="stepReviewPublicBodies && !stepWriteRequest" id="step-review-publicbody" class="mt-5">
            <pb-multi-review
              name="publicbody"
              :i18n="i18n"
              :scope="pbScope"
            >
            </pb-multi-review>
          </fieldset>

          <fieldset v-if="stepWriteRequest" id="step-request" class="mt-3">

            <slot name="request-legend-title"></slot>

            <div v-if="multiRequest && publicBodies.length > 1" class="publicbody-summary-container">
              <div class="publicbody-summary">
                <p>
                  {{ i18n._('toMultiPublicBodies', {count: publicBodies.length}) }}
                  <span v-if="!hidePublicbodyChooser">
                    <a class="pb-change-link badge badge-pill badge-primary ml-3" :href="config.url.makeRequest" @click.prevent="setStepSelectPublicBody">
                      {{ i18n.change }}
                    </a>
                  </span>
                </p>
              </div>
            </div>
            <div v-else class="publicbody-summary-container">
              <div class="row">
                <div class="col-lg-12 publicbody-summary">
                  <p>
                    {{ i18n._('toPublicBody', {name: publicBody.name}) }}
                    <span v-if="!hidePublicbodyChooser">
                      <a class="pb-change-link badge badge-pill badge-primary ml-3" :href="config.url.makeRequest" @click.prevent="setStepSelectPublicBody">
                        {{ i18n.change }}
                      </a>
                    </span>
                  </p>
                </div>
              </div>
              <div class="row" v-if="hasNotes">
                <div class="col-lg-8">
                  <div class="alert alert-warning" v-html="requestNotes">
                  </div>
                </div>
              </div>
            </div>

            <input v-for="pb in publicBodies" type="hidden" name="publicbody" :value="pb.id" :key="pb.id">
            <input type="hidden" name="law_type" :value="lawType">

            <div class="row">
              <div class="col-md-12">

                <div v-if="nonFieldErrors.length > 0" class="alert alert-danger">
                  <p v-for="error in nonFieldErrors" :key="error">{{ error }}</p>
                </div>

                <div class="form-group">
                  <label for="id_subject" :class="{ 'text-danger': errors.subject }">
                    {{ i18n.subject }}
                  </label>
                  <div v-if="editingDisabled">
                    <input type="hidden" name="subject" :value="subject"/>
                    <strong>{{ subject}}</strong>
                    <button @click.prevent="editingDisabled = false" class="btn btn-sm btn-white pull-right">
                      <small>{{ i18n.reviewEdit }}</small>
                    </button>
                  </div>
                  <input v-else v-model="subject" type="text" name="subject" class="form-control" id="id_subject" :class="{ 'is-invalid': errors.subject }" :placeholder="formFields.subject.placeholder" @keydown.enter.prevent/>
                </div>
              </div>
            </div>

            <div class="card mb-3">
              <div class="card-body">
                <div v-if="fullText && warnFullText" class="alert alert-warning">
                  <p>
                    {{ i18n.warnFullText }}
                  </p>
                </div>
                <div class="row">
                  <div v-if="!editingDisabled" class="col-md-4 order-md-2">
                    <transition name="saved-full-text">
                      <div v-if="savedFullTextBody">
                        <h6>
                          {{ i18n.savedFullTextChanges }}
                        </h6>
                        <textarea class="saved-body" v-model="savedFullTextBody" readonly></textarea>
                      </div>
                    </transition>
                    <slot name="requesthints"></slot>
                    <button v-if="fullTextDisabled" class="btn btn-light btn-sm" @click.prevent="resetFullText" >
                      {{ i18n.resetFullText }}
                    </button>
                  </div>
                  <div class="col-md-8 order-1">
                    <div v-if="!fullText" class="body-text">{{ letterStart }}</div>
                    <div v-if="editingDisabled" class="body-text">{{ body }}</div>
                    <textarea v-show="!editingDisabled" v-model="body" name="body" id="id_body" class="form-control body-textarea" :class="{ 'is-invalid': errors.body, 'attention': !hasBody }" :rows="bodyRows" @keyup="bodyChanged" :placeholder="formFields.body.placeholder"></textarea>
                    <label class="small pull-right text-muted" v-if="allowFullText && !editingDisabled">
                      <input type="checkbox" id="full_text_checkbox" name="full_text_checkbox" v-model="fullText" :disabled="fullTextDisabled">
                      <i v-if="warnFullText" class="fa fa-exclamation-triangle" aria-hidden="true"></i>
                      {{ formFields.full_text.label }}
                    </label>
                    <input type="hidden" name="full_text" v-model="fullText">
                    <div v-if="!fullText" class="body-text"><template v-if="!fullLetter"><a class="show-full-letter" href="#" @click.prevent="showFullLetter">[&hellip;]</a>
{{ letterEndShort }}</template><template v-else>
{{ letterEnd }}</template></div>
                    <div v-if="letterSignature" class="body-text"><em>{{ letterSignature }}</em></div>
                    <div v-if="!letterSignature && fullText" class="body-text">{{ letterSignatureName }}</div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-8">
                    <div class="form-group row" v-if="!user.id">
                      <div class="col" :class="{ 'text-danger': usererrors.first_name }">
                        <label class="control-label field-required" for="id_first_name" :class="{ 'text-danger': usererrors.first_name }">
                          {{ i18n.yourFirstName }}
                        </label>
                        <input v-model="first_name" type="text" name="first_name" class="form-control" :class="{ 'is-invalid': usererrors.first_name }" id="id_first_name" :placeholder="userformFields.first_name.placeholder" required/>
                        <p v-for="e in usererrors.first_name" :key="e.message">{{ e.message }}</p>
                      </div>

                      <div class="col" :class="{ 'text-danger': usererrors.last_name }">
                        <label class="control-label field-required" for="id_last_name" :class="{ 'text-danger': usererrors.last_name }">
                          {{ i18n.yourLastName }}
                        </label>
                        <input v-model="last_name" type="text" name="last_name" class="form-control" :class="{ 'is-invalid': usererrors.last_name }" id="id_last_name" :placeholder="userformFields.last_name.placeholder" required/>
                        <p v-for="e in usererrors.last_name" :key="e.message">{{ e.message }}</p>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-4 mt-4"  v-if="!user.id">
                    <small v-if="userformFields.last_name.help_text" v-html="userformFields.last_name.help_text"></small>
                  </div>
                </div>
              </div>
            </div>


            <user-registration v-if="!user.id" :form="userForm" :config="config"></user-registration>

            <div class="row">
              <div class="col-md-12">

                <slot name="public"></slot>

                <slot name="terms"></slot>
              </div>
            </div>

          </fieldset>

          <div class="row">
            <div class="col-md-12">
              <similar-requests v-if="showSimilar && stepWriteRequest" :pbScope="pbScope" :config="config"></similar-requests>
            </div>
          </div>

          <review-request v-if="stepWriteRequest" :pbScope="pbScope" :i18n="i18n"></review-request>

          <button v-if="stepWriteRequest && shouldCheckRequest" type="button" id="review-button" class="btn btn-primary" data-toggle="modal" data-target="#step-review">
            <i class="fa fa-check" aria-hidden="true"></i>
            {{ i18n.reviewRequest }}
          </button>
          <button v-else-if="stepWriteRequest" type="submit" id="send-request-button" class="btn btn-primary">
            <i class="fa fa-send" aria-hidden="true"></i>
            {{ i18n.submitRequest }}
          </button>
          <button v-if="stepWriteRequest && user.id && showDraft" type="submit" class="btn btn-secondary" name="save_draft" value="true">
            <i class="fa fa-save" aria-hidden="true"></i>
            {{ i18n.saveAsDraft }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SimilarRequests from './similar-requests'
import PublicbodyChooser from './publicbody/publicbody-chooser'
import PublicbodyMultiChooser from './publicbody/publicbody-multichooser'
import UserRegistration from './user-registration'
import ReviewRequest from './review-request'
import PbMultiReview from './publicbody/pb-multi-review'
import RequestFormBreadcrumbs from './request-form-breadcrumbs'

import {mapGetters, mapMutations, mapActions} from 'vuex'

import {
  STEPS, STEP_TO_URLS, SET_STEP_BY_URL,
  SET_STEP_SELECT_PUBLICBODY, SET_STEP_REVIEW_PUBLICBODY, SET_STEP_REQUEST,
  SET_PUBLICBODY, SET_PUBLICBODIES, CACHE_PUBLICBODIES,
  UPDATE_FIRST_NAME, UPDATE_LAST_NAME,
  SET_USER, UPDATE_SUBJECT, UPDATE_BODY, UPDATE_FULL_TEXT,
  UPDATE_LAW_TYPE, SET_CONFIG
} from '../store/mutation_types'

import LetterMixin from '../lib/letter-mixin'
import I18nMixin from '../lib/i18n-mixin'

const MAX_BODY_ROWS = 10
const MIN_BODY_ROWS = 3

export default {
  name: 'request-form',
  props: {
    config: {
      type: Object
    },
    publicbodyDefaultSearch: {
        type: String
    },
    publicbodyForm: {
      type: Object,
      default: null
    },
    publicbodies: {
      type: Array,
      default: null
    },
    userInfo: {
      type: Object,
      default: null
    },
    requestForm: {
      type: Object
    },
    userForm: {
      type: Object,
      default: null
    },
    showSimilar: {
      type: Boolean,
      default: false
    },
    showDraft: {
      type: Boolean,
      default: false
    },
    hidePublicbodyChooser: {
      type: Boolean,
      default: false
    },
    hideFullText: {
      type: Boolean,
      default: false
    },
    hideEditing: {
      type: Boolean,
      default: false
    },
    multiRequest: {
      type: Boolean,
      default: false
    }
  },
  components: {
    PublicbodyChooser,
    PublicbodyMultiChooser,
    UserRegistration,
    SimilarRequests,
    ReviewRequest,
    PbMultiReview,
    RequestFormBreadcrumbs
  },
  mixins: [I18nMixin, LetterMixin],
  data () {
    return {
      bodyRows: MIN_BODY_ROWS,
      bodyBeforeChange: '',
      savedFullTextBody: '',
      fullTextDisabled: false,
      editingDisabled: this.hideEditing,
      fullLetter: false
    }
  },
  created () {
    this.pbScope = 'make-request'
    this.setConfig(this.config)
    this.updateSubject(this.originalSubject)
    this.updateBody(this.originalBody)
    this.updateFullText(this.formFields.full_text.value || this.formFields.full_text.initial)
    if (this.userInfo !== null) {
      this.setUser(this.userInfo)
    }
    this.updateLawType(this.formFields.law_type.value || this.formFields.law_type.initial)
    if (this.publicbodies !== null) {
      let pbs = this.publicbodies
      this.setPublicBodies({
        publicBodies: pbs,
        scope: this.pbScope
      })
      this.cachePublicBodies(pbs)
    }
  },
  mounted () {
    let step = STEPS.SELECT_PUBLICBODY
    if (this.hasPublicBodies) {
      this.setStepRequest()
      step = STEPS.WRITE_REQUEST
    }
    window.onpopstate = (event) => {
      console.log('on pop state')
      let hash = document.location.hash
      let pathname = document.location.pathname
      this.setStepByUrl({hash, pathname})
    }
  },
  computed: {
    nonFieldErrors () {
      return this.form.nonFieldErrors
    },
    form () {
      return this.requestForm
    },
    formFields () {
      return this.form.fields
    },
    errors () {
      return this.form.errors
    },
    userformFields () {
      return this.userForm.fields
    },
    usererrors () {
      return this.userForm.errors
    },
    hasNotes () {
      if (this.defaultLaw) {
        return !!this.defaultLaw.request_note_html
      }
      // FIXME: find all notes of all public body default laws?
      return false
    },
    requestNotes () {
      if (this.defaultLaw) {
        return this.defaultLaw.request_note_html
      }
      return ''
    },
    publicBodySearch () {
      if (this.publicBody) {
        return this.publicBody.name
      }
      return this.publicbodyDefaultSearch
    },
    publicBodyListView () {
      if (this.multiRequest) {
        return 'multi'
      }
      return 'actionList'
    },
    subject: {
      get () {
        return this.$store.state.subject
      },
      set (value) {
        this.updateSubject(value)
      }
    },
    originalSubject () {
      return this.formFields.subject.value || this.formFields.subject.initial || ''
    },
    subjectWasChanged () {
      return this.subject !== this.formFields.subject.initial
    },
    hasBody () {
      return this.body && this.body.length > 0
    },
    originalBody () {
      return this.formFields.body.value || this.formFields.body.initial || ''
    },
    bodyWasChanged () {
      return this.body !== this.formFields.body.initial
    },
    body: {
      get () {
        return this.$store.state.body
      },
      set (value) {
        this.updateBody(value)
      }
    },
    allowFullText () {
      return this.user.id && !this.hideFullText
    },
    warnFullText () {
      return this.allowFullText && this.multipleLaws
    },
    multipleLaws () {
      return this.defaultLaw === null
    },
    fullText: {
      get () {
        return this.$store.state.fullText
      },
      set (value) {
        this.updateFullText(value)
        if (value) {
          this.bodyBeforeChange = this.body
          this.body = `${this.letterStart}\n${this.body}\n\n${this.letterEndNoName}`
        } else {
          if (!this.fullTextDisabled) {
            this.body = this.bodyBeforeChange
          }
        }
        let newLineCount = (this.body.match(/\n/g) || []).length
        this.bodyRows = Math.max(MIN_BODY_ROWS, Math.min(newLineCount + 1, MAX_BODY_ROWS))
      }
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
    hasPublicBodies () {
      return this.publicBodies.length > 0
    },
    publicBody () {
      return this.getPublicBodyByScope(this.pbScope)
    },
    publicBodies () {
      return this.getPublicBodiesByScope(this.pbScope)
    },
    shouldCheckRequest () {
      return this.bodyWasChanged || this.subjectWasChanged
    },
    ...mapGetters([
      'user',
      'getPublicBodyByScope',
      'getPublicBodiesByScope',
      'stepWriteRequest',
      'stepReviewPublicBodies',
      'stepSelectPublicBody',
      'step',
      'lawType'
    ])
  },
  methods: {
    resetFullText () {
      this.savedFullTextBody = this.body
      this.fullTextDisabled = false
      this.fullText = false
    },
    bodyChanged (e) {
      if (this.fullText) {
        this.fullTextDisabled = true
      }
      var ta = document.querySelector('[name=body]')
      while (ta.scrollHeight > ta.clientHeight && ta.rows < MAX_BODY_ROWS) {
        ta.style.overflow = 'hidden'
        ta.rows += 1
      }
      if (ta.scrollHeight > ta.clientHeight) {
        ta.style.overflow = 'auto'
      }
      this.bodyRows = ta.rows
    },
    showFullLetter () {
      this.fullLetter = true
    },
    goToRequestPbUrl (args) {
      if (this.publicBody === null) {
        this.setPublicBodyById({scope: this.pbScope, id: parseInt(args[1])})
      } else {
        this.setStepRequest()
      }
    },
    gotToSelectPbUrl () {
      if (this.hidePublicbodyChooser) {
        return
      }
      this.setStepSelectPublicBody()
    },
    setStepByUrl ({hash, pathname}) {
      const pbUrl = '^' + this.config.url.makeRequestTo.replace(/0/, '([\\d\\+]+)') + '$'
      const startUrl = '^' + this.config.url.makeRequest + '$'
      const URLS = {
        [pbUrl]: 'goToRequestPbUrl',
        [startUrl]: 'gotToSelectPbUrl'
      }
      this.ignoreWatchStep = true
      for (let regex in URLS) {
        let res = (new RegExp(regex)).exec(pathname)
        if (res) {
          this[URLS[regex]](res)
          break
        }
      }
      this.ignoreWatchStep = false
    },
    ...mapMutations({
      setStepSelectPublicBody: SET_STEP_SELECT_PUBLICBODY,
      setStepRequest: SET_STEP_REQUEST,
      updateSubject: UPDATE_SUBJECT,
      updateBody: UPDATE_BODY,
      updateFullText: UPDATE_FULL_TEXT,
      setConfig: SET_CONFIG,
      setUser: SET_USER,
      updateFirstName: UPDATE_FIRST_NAME,
      updateLastName: UPDATE_LAST_NAME,
      updateLawType: UPDATE_LAW_TYPE,
      setPublicBody: SET_PUBLICBODY,
      setPublicBodies: SET_PUBLICBODIES,
      cachePublicBodies: CACHE_PUBLICBODIES
    }),
    ...mapActions([
      'setPublicBodyById'
    ])
  },
  watch: {
    step (newStep, oldStep) {
      if (this.ignoreWatchStep) {
        return
      }
      if (oldStep === newStep) {
        return
      }
      let nextUrl
      if (newStep === STEPS.SELECT_PUBLICBODY) {
        nextUrl = this.config.url.makeRequest
      } else if (newStep === STEPS.WRITE_REQUEST && oldStep < newStep) {
        if (this.publicBody === null) {
          console.error('WARNING', newStep, oldStep)
          return
        }
        if (this.multiRequest) {
          return
        }
        nextUrl = this.config.url.makeRequestTo.replace(/0/, this.publicBody.id)
      }
      if (nextUrl === undefined || nextUrl === document.location.pathname) {
        return
      }
      if (this.hidePublicbodyChooser) {
        window.history.replaceState(null, '', nextUrl + document.location.search)
      } else {
        window.history.pushState(null, '', nextUrl + document.location.search)
      }
      window.scrollTo(0, 0)
    }
  }
}
</script>

<style lang="scss" scoped>

@import "../../styles/variables";

.make-request-container {
  padding-bottom: 1rem;
}

.container-multi {
  /* Allow container to wider than normal to allow for more space */
  width: 100%;
  padding-right: 15px;
  padding-left: 15px;
  margin-right: auto;
  margin-left: auto;
  max-width: 1400px;
}

legend {
  padding: 2rem 0 2rem;
  font-size: 2rem;
}

.small a {
  color: $blue;
}

.request-hints {
  color: $gray-700;
  font-size: $font-size-sm;
  ul {
    padding-left: $spacer;
  }
}

.publicbody-summary-container {
  margin: 0 0 $spacer*2;
}

.publicbody-summary {
  font-size: $font-size-lg;
}

.pb-change-link {
  font-weight: normal;
  font-size: $font-size-sm;
}

.body-text {
  white-space: pre-wrap;
  word-wrap: break-word;
  color: #999;
}

.body-textarea {
  width: 100%;
}

.body-textarea {
  padding-left: 0;
  margin-left: -5px;
  padding: 5px;
}
.body-textarea.attention {
  border-left: 3px solid #faa;
}

.saved-body {
  width: 100%;
  height: 5em;
}

.saved-full-text-enter-active, .saved-full-text-leave-active {
  transition: opacity .5s;
}
.saved-full-text-enter, .saved-full-text-leave-to {
  opacity: 0;
}

.show-full-letter {
  color: #999;
  text-decoration: underline;
}

</style>
