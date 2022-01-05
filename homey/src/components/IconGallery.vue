<template>
    <div class="icon-gallery">
        <div class="icon-gallery__icon" v-for="i in icons" :key=icons.indexOf(i) :title="i">
            <img :src="'./images/icons/' + i" @click="pickIcon(i)" />
        </div>
    </div>
</template>

<script>
export default {
    name: 'IconGallery',
    props: {
    },
    data: function() {
        return {
            icons: [],
            icon: String,
        };
    },
    methods: {
        getIcons() {
            this.axios.get('http://0.0.0.0:9101/getIconPath/all').then((res) => {
                this.icons = res.data;
            }).catch(e => {
                console.log('Could not reach homey API');
            });
        },
        pickIcon(name){
            this.icon = name;
            // TODO: this should be emitted
            this.$parent.selectNewIcon(this.icon);
            this.$parent.showGallery = false;
        }
    },
    created() {
        this.getIcons();
    }
}
</script>