import Vue from 'vue';
import camelCase from 'lodash/camelCase';
import upperFirst from 'lodash/upperFirst';

const requireComponent = require.context('@/components', true, /\.vue$/);
requireComponent.keys().forEach((fileName) => {
  const componentConfig = requireComponent(fileName);
  const componentName = upperFirst(camelCase(fileName.replace(/^\.\//, '').replace(/\.\w+$/, '')));
  Vue.component(componentName, componentConfig.default || componentConfig);
});
