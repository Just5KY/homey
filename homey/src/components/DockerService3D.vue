<template>
<Group>
    <Box @pointerEnter="mouseoverBox" @pointerLeave="mouseleaveBox"
          ref="boxInner"
          :position="{ x: this.gridIndex - 2.6 }"
          :size="this.size">
          <!-- convert to matcap / baked in material & nix light -->
          <LambertMaterial />
    </Box>
    <Text
        ref="detailContainer"
        v-if="mouseIn"
        :text="this.serviceName"
        font-src="./fonts/helvetiker.json"
        align="center"
        :size=".2"
        :height="0.02"
        :position="{x: this.gridIndex - 3.05}"
        :rotation="{y: Math.PI / -2}"
        :visible="false"
        :cast-shadow="true">
        <LambertMaterial />
    </Text>
</Group>
</template>

<script>
export default {
    name: 'DockerService3D',
    props: {
        serviceName: String,
        gridIndex: Number,
        size: Number,
    },
    data: function() {
        return {
            mouseIn: false,
        };
    },
    methods: {
        mouseoverBox(event) {
            this.mouseIn = true;
            this.$refs.boxInner.mesh.scale.z = this.widthToScale(this.serviceName.length);
        },
        mouseleaveBox(event) {
            this.$refs.boxInner.mesh.scale.z = 1;
            this.mouseIn = false;
        },
        widthToScale(number) {
            // map a service name of length 0-255 to a scale factor which will appropriately resize box
            let fromRange = [0, 255];
            let toRange = [2, 45];
            return (((number - fromRange[0]) * (toRange[1] - toRange[0])) /
                (fromRange[1] - fromRange[0]) + toRange[0]);
        },
    }
}
</script>