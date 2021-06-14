<template>
  <component :is="variant" :class="arrClass">
    <slot />
  </component>
</template>

<script>

export default {
  props: {
    variant: {
      type: String,
      default: 'span',
      require: false
    },
    fontWeight: {
      type: String,
      default: undefined,
      require: false,
      validator: (val) => ['light', 'default', 'medium', 'semi-bold', 'bold'].includes(val)
    },
    fontSize: {
      type: String,
      default: undefined,
      require: false,
      validator: (val) => ['extra-small', 'small', 'default', 'medium', 'larger', 'extra-larger', 'huge'].includes(val)
    },
    lineHeight: {
      type: String,
      default: undefined,
      require: false,
      validator: (val) => ['compact', 'regular', 'loose'].includes(val)
    },
    convention: {
      type: String,
      default: undefined,
      require: false,
      validator: (val) => ['small-title', 'title', 'main-title'].includes(val)
    }
  },
  computed: {
    arrClass() {
      const fontSize = this.fontSize ? `font-size-${this.fontSize}` : 'font-size'
      const lineHeight = this.lineHeight ? `line-height-${this.lineHeight}` : 'line-height'
      const fontWeight = this.fontWeight ? `font-weight-${this.fontWeight}` : 'font-weight'

      const arr = [fontSize, lineHeight, fontWeight]

      if (this.convention) arr.push(this.convention)

      return arr
    }
  }
}

</script>

<style lang="scss" scoped>
$font-size-extra-small: 12px;
$font-size-small: 13px;
$font-size-default: 14px;
$font-size-medium: 16px;
$font-size-larger: 18px;
$font-size-extra-larger: 20px;
$font-size-huge: 24px;

$font-weight-light: 300;
$font-weight-default: 400;
$font-weight-medium: 500;
$font-weight-semi-bold: 600;
$font-weight-bold: 700;

$line-height-default: 1px;
$line-height-compact: 1.3px;
$line-height-regular: 1.5px;
$line-height-loose: 1.7px;

.font-size {
    font-size: $font-size-default;

    &-extra-small{
        font-size: $font-size-extra-small;
    }

    &-small{
        font-size: $font-size-small;
    }

    &-medium{
        font-size: $font-size-medium;
    }

    &-larger{
        font-size: $font-size-larger;
    }

    &-extra-larger{
        font-size: $font-size-extra-larger;
    }

    &-huge{
        font-size: $font-size-huge;
    }
}

.font-weight {
    font-weight: $font-weight-default;

    &-light{
        font-weight: $font-weight-light;
    }

    &-medium{
        font-weight: $font-weight-medium;
    }

    &-semi-bold{
        font-weight: $font-weight-semi-bold;
    }

    &-bold{
        font-weight: $font-weight-bold;
    }
}

.line-height {
    line-height: $line-height-default;

    .compact{
        line-height: $line-height-compact;
    }

    .regular{
        line-height: $line-height-regular;
    }

    .loose {
        line-height: $line-height-loose;
    }
}

.small-title {
  font-size: $font-size-larger;
  font-weight: $font-weight-medium;
  line-height: $line-height-compact;
}

.title {
  font-size: $font-size-extra-larger;
  font-weight: $font-weight-semi-bold;
  line-height: $line-height-regular;
}

.main-title {
  font-size: $font-size-huge;
  font-weight: $font-weight-bold;
  font-weight: $line-height-loose;
}

</style>
