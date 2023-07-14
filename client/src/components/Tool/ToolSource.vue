<template>
    <ToolSourceProvider :id="toolId" v-slot="{ result, loading, error }">
        <loading-span v-if="loading" message="Waiting on tool source" />
        <GAlert v-else-if="error" :message="error" variant="error" />
        <tool-source-display v-else :language="result.language" :code="result.source" />
    </ToolSourceProvider>
</template>
<script>
import LoadingSpan from "components/LoadingSpan";
import { ToolSourceProvider } from "components/providers/ToolSourceProvider";

import GAlert from "@/component-library/GAlert.vue";

export default {
    components: {
        GAlert,
        LoadingSpan,
        ToolSourceProvider,
        ToolSourceDisplay: () => import(/* webpackChunkName: "ToolSourceDisplay" */ "./ToolSourceDisplay.vue"),
    },
    props: {
        toolId: {
            type: String,
            required: true,
        },
    },
};
</script>
