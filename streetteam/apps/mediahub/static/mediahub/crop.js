import 'cropperjs/dist/cropper.css';
import Cropper from 'cropperjs';

const image = document.getElementById('image');
const cropper = new Cropper(image, {
  viewMode: 1,
  dragMode: 'crop',
  initialAspectRatio: 16 / 9
});
