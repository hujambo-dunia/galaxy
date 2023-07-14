<template>
    <GInput v-model="localValue" class="directory-form-input" :placeholder="placeholder" @click="selectFile" />
</template>

<script>
import GInput from "component-library/GInput";
import { filesDialog } from "utils/data";

export default {
    components: { GInput },
    props: {
        value: {
            type: String,
        },
        mode: {
            type: String,
            default: "file",
        },
        requireWritable: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            localValue: this.value,
        };
    },
    computed: {
        placeholder() {
            return `Click to select ${this.mode}`;
        },
    },
    watch: {
        localValue(newValue) {
            this.$emit("input", newValue);
        },
        value(newValue) {
            this.localValue = newValue;
        },
    },
    methods: {
        selectFile() {
            const props = {
                mode: this.mode,
                requireWritable: this.requireWritable,
            };
            filesDialog((selected) => {
                this.localValue = selected?.url;
            }, props);
        },
    },
};
</script>
