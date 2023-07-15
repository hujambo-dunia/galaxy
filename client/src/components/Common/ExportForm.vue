<template>
    <div class="export-to-remote-file">
        <b-form-group
            id="fieldset-directory"
            label-for="directory"
            :description="directoryDescription | localize"
            class="mt-3">
            <files-input id="directory" v-model="directory" mode="directory" :require-writable="true" />
        </b-form-group>
        <b-form-group id="fieldset-name" label-for="name" :description="nameDescription | localize" class="mt-3">
            <GInput id="name" v-model="name" :placeholder="namePlaceholder | localize" required />
        </b-form-group>
        <GRow align-h="end">
            <GCol>
                <b-button class="export-button" variant="primary" :disabled="!canExport" @click.prevent="doExport">
                    {{ exportButtonText | localize }}
                </b-button>
            </GCol>
        </GRow>
    </div>
</template>

<script>
import GInput from "component-library/GInput";

import GCol from "@/component-library/GCol.vue";
import GRow from "@/component-library/GRow.vue";
import FilesInput from "components/FilesDialog/FilesInput.vue";

export default {
    components: {
        GRow,
        GCol,
        FilesInput,
        GInput,
    },
    props: {
        what: {
            type: String,
            default: "archive",
        },
        clearInputAfterExport: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            directory: null,
            name: null,
        };
    },
    computed: {
        directoryDescription() {
            return `Select a 'remote files' directory to export ${this.what} to.`;
        },
        nameDescription() {
            return "Give the exported file a name.";
        },
        namePlaceholder() {
            return "Name";
        },
        exportButtonText() {
            return "Export";
        },
        canExport() {
            return !!this.name && !!this.directory;
        },
    },
    methods: {
        doExport() {
            this.$emit("export", this.directory, this.name);
            if (this.clearInputAfterExport) {
                this.directory = null;
                this.name = null;
            }
        },
    },
};
</script>
