<script setup>
import { BNavbar, BNavbarBrand, BNavbarNav } from "bootstrap-vue";
import MastheadItem from "./MastheadItem";
import { loadWebhookMenuItems } from "./_webhooks";
import QuotaMeter from "./QuotaMeter";
import { getActiveTab } from "./utilities";
import { watch, ref, reactive, computed } from "vue";
import { onMounted, onBeforeMount } from "vue";
import { useRoute } from "vue-router/composables";
import { useEntryPointStore } from "stores/entryPointStore";
import { getAppRoot } from "onload/loadConfig";

const route = useRoute();
const emit = defineEmits(["open-url"]);

const props = defineProps({
    tabs: {
        type: Array,
        default: () => [],
    },
    brand: {
        type: String,
        default: null,
    },
    initialActiveTab: {
        type: String,
        default: "analysis",
    },
    logoUrl: {
        type: String,
        default: null,
    },
    logoSrc: {
        type: String,
        default: null,
    },
    logoSrcSecondary: {
        type: String,
        default: null,
    },
    windowTab: {
        type: Object,
        default: null,
    },
});

const activeTab = ref(props.initialActiveTab);
const extensionTabs = ref([]);
const windowToggle = ref(false);
const anvilLink = ref("https://anvil.terra.bio");
const navGuardModal = ref(null);

let entryPointStore;
const itsMenu = reactive({
    id: "interactive",
    url: "/interactivetool_entry_points/list",
    tooltip: "See Running Interactive Tools",
    icon: "fa-cogs",
    hidden: true,
});

const anvilLogoSrc = computed(() => `${getAppRoot()}static/images/anvilwhite.png`);
const galaxyLogoSrc = computed(() => `${getAppRoot()}static/images/galaxy_project_logo_white_square.png`);

function setActiveTab() {
    const currentRoute = route.path;
    activeTab.value = getActiveTab(currentRoute, props.tabs) || activeTab.value;
}

function onWindowToggle() {
    windowToggle.value = !windowToggle.value;
}
function updateVisibility(isActive) {
    itsMenu.hidden = !isActive;
}

function showNavGuard(ev) {
    const dismissNavGuard = localStorage.getItem("dismissNavGuard");
    if (!dismissNavGuard === true) {
        navGuardModal.value.show();
        ev.preventDefault();
    }
}

function confirmNav() {
    localStorage.setItem("dismissNavGuard", true);
    window.location = anvilLink.value;
}

watch(
    () => route.path,
    () => {
        setActiveTab();
    }
);

/* lifecyle */
onBeforeMount(() => {
    entryPointStore = useEntryPointStore();
    entryPointStore.ensurePollingEntryPoints();
    entryPointStore.$subscribe((mutation, state) => {
        updateVisibility(state.entryPoints.length > 0);
    });
});
onMounted(() => {
    loadWebhookMenuItems(extensionTabs.value);
    setActiveTab();
});
</script>

<template>
    <b-navbar id="masthead" type="dark" role="navigation" aria-label="Main" class="justify-content-between">
        <b-navbar-nav>
            <b-navbar-brand :href="anvilLink" aria-label="homepage" @click="showNavGuard">
                <img alt="Galaxy Logo" style="padding-top: 0.4rem" class="navbar-brand-image" :src="galaxyLogoSrc" />
                <img alt="Anvil Logo" class="navbar-brand-image" :src="anvilLogoSrc" />
            </b-navbar-brand>
            <span v-if="brand" class="navbar-text">
                {{ brand }}
            </span>
        </b-navbar-nav>
        <b-modal ref="navGuardModal" hide-footer title="A quick note before you go">
            <div>
                <p>
                    You are navigating away from Galaxy, which will continue to run in the background. Any jobs you have
                    running will continue, but it's important to keep in mind that this instance will also continue
                    potentially incurring costs. Remember to shut down Galaxy when you are done.
                </p>
                <p>This modal will not be shown again.</p>
            </div>
            <b-button variant="primary" block @click="confirmNav">
                I understand, take me back to my AnVIL Dashboard
            </b-button>
        </b-modal>
        <b-navbar-nav>
            <masthead-item
                v-for="(tab, idx) in props.tabs"
                v-show="tab.hidden !== true"
                :key="`tab-${idx}`"
                :tab="tab"
                :active-tab="activeTab"
                @open-url="emit('open-url', $event)" />
            <masthead-item
                v-show="itsMenu.hidden !== true"
                :key="`its-tab`"
                :tab="itsMenu"
                :active-tab="activeTab"
                @open-url="emit('open-url', $event)" />
            <masthead-item
                v-for="(tab, idx) in extensionTabs"
                v-show="tab.hidden !== true"
                :key="`extension-tab-${idx}`"
                :tab="tab"
                :active-tab="activeTab"
                @open-url="emit('open-url', $event)" />
            <masthead-item v-if="windowTab" :tab="windowTab" :toggle="windowToggle" @click="onWindowToggle" />
        </b-navbar-nav>
        <quota-meter />
    </b-navbar>
</template>

<style scoped lang="scss">
@import "theme/blue.scss";

#masthead {
    padding: 0;
    margin-bottom: 0;
    background: var(--masthead-color);
    height: $masthead-height;
    &:deep(.navbar-nav) {
        height: $masthead-height;
        & > li {
            // This allows the background color to fill the full height of the
            // masthead, while still keeping the contents centered (using flex)
            min-height: 100%;
            display: flex;
            align-items: center;
            background: var(--masthead-link-color);
            &:hover {
                background: var(--masthead-link-hover);
            }
            &.show,
            &.active {
                background: var(--masthead-link-active);
                .nav-link {
                    color: var(--masthead-text-active);
                }
            }
            .nav-link {
                position: relative;
                cursor: pointer;
                text-decoration: none;
                color: var(--masthead-text-color);
                &:hover {
                    color: var(--masthead-text-hover);
                }
                &.nav-icon {
                    font-size: 1.3em;
                    .nav-note {
                        position: absolute;
                        left: 1.9rem;
                        top: 1.9rem;
                        font-size: 0.6rem;
                        font-weight: bold;
                    }
                }
                &.toggle {
                    color: var(--masthead-text-hover);
                }
            }
        }
    }
    .navbar-brand {
        cursor: pointer;
        img {
            display: inline;
            border: none;
            height: 2.3rem;
        }
    }
    .navbar-text {
        font-weight: bold;
        font-family: Verdana, sans-serif;
        font-size: 1rem;
        line-height: 2rem;
        color: var(--masthead-text-color);
    }
}
</style>
