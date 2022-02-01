<template>
    <div class="icon-gallery">
        <div class="icon-gallery__icon" v-for="i in icons" :key=icons.indexOf(i) :title="i">
            <img :src="'./data/icons/' + i" @click="pickIcon(i)" />
        </div>
    </div>
</template>

<script>
export default {
    name: 'IconGallery',
    emits: ['selectIcon'],
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
            this.axios.get('/api/getIconPath/all').then((res) => {
                this.icons = res.data;
            }).catch(e => {
                console.log('Could not reach homey API');
            });
        },
        pickIcon(name){
            this.icon = name;
            this.$emit('selectIcon', name)
        }
    },
    created() {
        this.getIcons();
    }
}
</script>