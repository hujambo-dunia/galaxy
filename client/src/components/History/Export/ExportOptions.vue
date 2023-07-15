<script setup>
import { BCollapse, BFormCheckbox, BFormGroup, BFormSelect } from "bootstrap-vue";
import { ExportParamsModel } from "components/Common/models/exportRecordModel";
import { computed, reactive, ref } from "vue";

import { AVAILABLE_EXPORT_FORMATS } from "./services";

import GCard from "@/component-library/GCard.vue";
import GLink from "@/component-library/GLink.vue";

const props = defineProps({
    exportParams: {
        type: ExportParamsModel,
        required: true,
    },
});

const emit = defineEmits(["onValueChanged"]);

const isExpanded = ref(false);
const title = computed(() => (isExpanded.value ? `Hide advanced export options` : `Show advanced export options`));
const localOptions = reactive({
    modelStoreFormat: props.exportParams.modelStoreFormat,
    includeFiles: props.exportParams.includeFiles,
    includeDeleted: props.exportParams.includeDeleted,
    includeHidden: props.exportParams.includeHidden,
});

function onValueChanged() {
    emit("onValueChanged", localOptions);
}
</script>

<template>
    <div>
        <GLink
            id="toggle-options-link"
            :class="isExpanded ? null : 'collapsed'"
            :aria-expanded="isExpanded ? 'true' : 'false'"
            aria-controls="collapse-options"
            @click="isExpanded = !isExpanded">
            {{ title }}
        </GLink>
        <b-collapse id="collapse-options" v-model="isExpanded">
            <GCard>
                <b-form-group label="Export Format:" label-for="format">
                    <b-form-select
                        id="format-selector"
                        v-model="localOptions.modelStoreFormat"
                        :options="AVAILABLE_EXPORT_FORMATS"
                        value-field="id"
                        text-field="name"
                        @change="onValueChanged" />
                </b-form-group>

                <b-form-group label="Dataset files included in the package:">
                    <b-form-checkbox
                        id="include-files-check"
                        v-model="localOptions.includeFiles"
                        switch
                        @change="onValueChanged">
                        Include Active
                    </b-form-checkbox>

                    <b-form-checkbox
                        id="include-deleted-check"
                        v-model="localOptions.includeDeleted"
                        switch
                        @change="onValueChanged">
                        Include Deleted (not purged)
                    </b-form-checkbox>

                    <b-form-checkbox
                        id="include-hidden-check"
                        v-model="localOptions.includeHidden"
                        switch
                        @change="onValueChanged">
                        Include Hidden
                    </b-form-checkbox>
                </b-form-group>
            </GCard>
        </b-collapse>
    </div>
</template>
