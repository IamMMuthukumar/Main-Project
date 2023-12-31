#
#         Luxand FaceSDK Library
#
#  Copyright(c) 2020 Luxand, Inc.
#         http://www.luxand.com
#
#  Wrapper classes and functions for FSDK
#  This code is compatible with python 2 & 3 
#
###########################################

import ctypes, os, sys, inspect
from ctypes import c_int, c_uint, c_ushort, c_float, c_char, c_longlong, c_double, c_ubyte, c_wchar, c_wchar_p, c_bool, c_void_p
from ctypes import POINTER, byref, create_string_buffer
from . import const

python2 = sys.version_info.major == 2
windows = sys.platform == 'win32'
if windows:
	from ctypes import wintypes, windll
	import win
	from win import HBITMAP

# supported platforms returned by sys.platform attribute
FSDK_LIB = {
	'win32': 'win32/facesdk.dll',
	'win64': 'win64/facesdk.dll',
	'darwin': 'osx_x86_64/libfsdk.dylib',
	'linux32': 'linux32/libfsdk.so',
	'linux64': 'linux64/libfsdk.so',
	'linux32_arm': 'linux32_arm/libfsdk.so',
	'linux64_arm': 'linux64_arm/libfsdk.so',
}

platform = sys.platform
if platform == 'win32':
	if '64 bit' in sys.version:
		platform = 'win64'
elif 'linux' in platform:
	platform = 'linux64' if sys.maxsize > 2**32 else 'linux32'
	import platform as _platform
	if 'arm' in _platform.machine():
		platform += '_arm'

if platform not in FSDK_LIB: 
	raise Exception("Unsupported platform '%s' for FSDK.\nMake sure your platform is specified in FSDK_LIB dictionary." % sys.platform)
fsdkDll_file_name = os.path.join(os.path.split(__file__)[0], FSDK_LIB[platform])
if not os.path.isfile(fsdkDll_file_name):  
	raise Exception("FSDK binary '%s' could not be found." % fsdkDll_file_name)
fsdkDll = ctypes.CDLL(fsdkDll_file_name)

ERROR_NAMES = {v:n for n,v in const.__dict__.items() if n.startswith('FSDKE_')}

# this exception class is available as FSDK.Exception
class FSDK_Exception(Exception):
	def __init__(self, func_name, error_id, desc=''):
		self.func_name, self.error_id = func_name, error_id
		msg = "%s -> %s (%s)" % (func_name, ERROR_NAMES.get(error_id, 'UNKNOWN ERROR'), desc or error_id)
		if error_id == const.FSDKE_NOT_ACTIVATED: msg += '\nPlease run the License Key Wizard (Start - Luxand - FaceSDK - License Key Wizard)'
		super(FSDK_Exception, self).__init__(msg)

# exceptions generated by wrapper for particular FaceSDK error codes
class Failed(FSDK_Exception): pass 				# FSDKE_FAILED = -1
class NotActivated(FSDK_Exception): pass  		# FSDKE_NOT_ACTIVATED = -2
class OutOfMemory(FSDK_Exception): pass  		# FSDKE_OUT_OF_MEMORY = -3
class InvalidArgument(FSDK_Exception): pass 	# FSDKE_INVALID_ARGUMENT = -4
class IOError(FSDK_Exception): pass 			# FSDKE_IO_ERROR = -5
class ImageTooSmall(FSDK_Exception): pass 		# FSDKE_IMAGE_TOO_SMALL = -6
class FaceNotFound(FSDK_Exception): pass 		# FSDKE_FACE_NOT_FOUND = -7
class InsufficientBufferSize(FSDK_Exception): pass # FSDKE_INSUFFICIENT_BUFFER_SIZE = -8
class UnsupportedImageExtension(FSDK_Exception): pass # FSDKE_UNSUPPORTED_IMAGE_EXTENSION = -9
class CannotOpenFile(FSDK_Exception): pass 		# FSDKE_CANNOT_OPEN_FILE = -10
class CannotCreateFile(FSDK_Exception): pass 	# FSDKE_CANNOT_CREATE_FILE = -11
class BadFileFormat(FSDK_Exception): pass 		# FSDKE_BAD_FILE_FORMAT = -12
class FileNotFound(FSDK_Exception): pass 		# FSDKE_FILE_NOT_FOUND = -13
class ConnectionClosed(FSDK_Exception): pass 	# FSDKE_CONNECTION_CLOSED = -14
class ConnectionFailed(FSDK_Exception): pass 	# FSDKE_CONNECTION_FAILED = -15
class IPInitFailed(FSDK_Exception): pass 		# FSDKE_IP_INIT_FAILED = -16
class NeedServerActivation(FSDK_Exception): pass # FSDKE_NEED_SERVER_ACTIVATION = -17
class IdNotFound(FSDK_Exception): pass 			# FSDKE_ID_NOT_FOUND = -18
class AttributeNotDetected(FSDK_Exception): pass # FSDKE_ATTRIBUTE_NOT_DETECTED = -19
class InsufficientTrackerMemoryLimit(FSDK_Exception): pass # FSDKE_INSUFFICIENT_TRACKER_MEMORY_LIMIT = -20
class UnknownAttribute(FSDK_Exception): pass 	# FSDKE_UNKNOWN_ATTRIBUTE = -21
class UnsupportedFileVersion(FSDK_Exception): pass # FSDKE_UNSUPPORTED_FILE_VERSION = -22
class SyntaxError(FSDK_Exception): pass 		# FSDKE_SYNTAX_ERROR = -23
class ParameterNotFound(FSDK_Exception): pass 	# FSDKE_PARAMETER_NOT_FOUND = -24
class InvalidTemplate(FSDK_Exception): pass 	# FSDKE_INVALID_TEMPLATE = -25
class UnsupportedTemplateVersion(FSDK_Exception): pass # FSDKE_UNSUPPORTED_TEMPLATE_VERSION = -26
class CameraIndexDoesNotExist(FSDK_Exception): pass # FSDKE_CAMERA_INDEX_DOES_NOT_EXIST = -27
class PlatformNotLicensed(FSDK_Exception): pass # FSDKE_PLATFORM_NOT_LICENSED = -28

def value_to_str(val):
	val = str(val)
	return val.lower() if val in ('True', 'False') else val

# types used in FSDK
class Point(ctypes.Structure):
	_fields_ = ("x", c_int), ("y", c_int)
	__repr__ = __str__ = lambda p: 'Point(x=%i, y=%i)' % (p.x, p.y)

class Eyes(Point*2):
	if python2:
		_type_ = Point*2
		_length_ = ctypes.sizeof(_type_)
	__repr__ = __str__ = lambda p: 'Eyes(%s, %s)' % (p[0], p[1])

class FacePosition(ctypes.Structure):
 	_fields_ = ("xc", c_int), ("yc", c_int), ("w", c_int), ("_padding", c_int), ("angle", c_double)
 	__repr__ = __str__ = lambda x: 'FacePosition(xc=%i, yc=%i, w=%i, angle=%.1f)' % (x.xc, x.yc, x.w, x.angle)
 	@property
 	def rect(self):	x, y, w = self.xc, self.yc, self.w//2; return x-w, y-w, x+w, y+w

Features = Point*const.FSDK_FACIAL_FEATURE_COUNT
ConfidenceLevels = c_float*const.FSDK_FACIAL_FEATURE_COUNT
FaceTemplate = c_char*const.FSDK_FACE_TEMPLATE_SIZE
# the following code is needed for python2 compatibility
FaceTemplate.MatchFaces = FaceTemplate.Match = lambda self, face_template: FSDK.MatchFaces(self, face_template)
FaceTemplate.__name__ = 'FaceTemplate'
Features.__name__ = 'Features'

class Camera(ctypes.Structure):
	_fields_ = ("handle", c_int), # FSDK camera handle
	def __init__(self, cameraName=None): # cameraName is for windows only
		if cameraName is None: super(Camera, self).__init__(-1)
		elif isinstance(cameraName, str):
			cam = FSDK.OpenVideoCamera(cameraName)
			super(Camera, self).__init__(cam.handle)
			self.name, cam.handle = cameraName, -1
			if hasattr(cameraName, 'device_path'): self.device_path = cameraName.device_path
		else: raise InvalidArgument('Camera construction', const.FSDKE_INVALID_ARGUMENT, desc = str(cameraName))
	Close = __del__ = lambda self: FSDK.CloseVideoCamera(self) # destructor
	def Open(self, cameraName):
		self.Close()
		cam = FSDK.OpenVideoCamera(cameraName)
		self.cam, cam.handle = cam.handle, -1
	def GrabFrame(self): return FSDK.GrabFrame(self)

if windows: # windows specific classes
	# class HBITMAP(wintypes.HBITMAP):
	# 	def __del__(self): windll.gdi32.DeleteObject(self)
	class VideoFormatInfo(ctypes.Structure):
	 	_fields_ = ("Width", c_int), ("Height", c_int), ("BPP", c_int)
	 	__repr__ = __str__ = lambda x: 'VideoFormatInfo(Width=%i, Height=%i, BPP=%i)' % (x.Width, x.Height, x.BPP)

class Image(ctypes.Structure):
	_fields_ = ("handle", c_int), # FSDK image handle (-1 means invalid or uninitialized handle)
	def __new__(cls, arg = None):
		if arg is None: return FSDK.CreateEmptyImage()
		if type(arg) is int: return super(Image, cls).__new__(cls)
		if type(arg) is str: return FSDK.LoadImageFromFile(arg)
		if windows and type(arg) is HBITMAP: return FSDK.LoadImageFromHBitmap(arg)
		raise InvalidArgument('Image construction', const.FSDKE_INVALID_ARGUMENT, desc = str(arg))
	def __init__(self, arg=None): super(Image, self).__init__(self.handle)
	Free = __del__ = lambda self: FSDK.FreeImage(self) # the function is called implicitly whenever Image is garbage collected, but can be called explicitly too
	__repr__ = __str__ = lambda x: 'Image(handle=%x)' % x.handle
	def swap(self, image): self.handle, image.handle = image.handle, self.handle; return self # swap FSDK handles of images

	width = property(lambda self: FSDK.GetImageWidth(self)) # image width
	height = property(lambda self: FSDK.GetImageHeight(self))  # image height
	size = property(lambda self: (self.width, self.height))  # image size = (width, height)

	@staticmethod
	def FromFile(fileName): return FSDK.LoadImageFromFile(fileName)
	@staticmethod
	def FromBuffer(buffer, width, height, scanLine, colorMode): return FSDK.LoadImageFromBuffer(buffer, width, height, scanLine, colorMode)
	FromBytes = FromBuffer

	def SaveToFile(self, fileName, quality = None):
		if quality: FSDK.SetJpegCompressionQuality(quality)
		FSDK.SaveImageToFile(self, fileName)

	#### Copy functions
	def Copy(self): return FSDK.CopyImage(self, Image())
	def CopyRect(self, x1, y1, x2, y2): return FSDK.CopyRect(self, x1, y1, x2, y2, Image())
	def CopyRectReplicateBorder(self, x1, y1, x2, y2): return FSDK.CopyRectReplicateBorder(self, x1, y1, x2, y2, Image())

	def Mirror(self, useVerticalMirroringInsteadOfHorizontal=False): return FSDK.MirrorImage(self, useVerticalMirroringInsteadOfHorizontal)
	def Resize(self, ratio): return FSDK.ResizeImage(self, ratio, Image())
	def ResizeXY(self, ratioX, ratioY): return FSDK.ResizeImageXY(self, ratioX, ratioY, Image())
	def Rotate90(self, multiplier = 1): return FSDK.RotateImage90(self, multiplier, Image())
	def Rotate(self, angle): return FSDK.RotateImage(self, angle, Image())
	def RotateCenter(self, angle, xc, yc): return FSDK.RotateCenter(self, angle, xc, yc, Image())
	def Crop(self, x1, y1, x2, y2): return FSDK.CopyRect(self, x1, y1, x2, y2, Image())
	def CropReplicateBorder(self, x1, y1, x2, y2): return FSDK.CopyRectReplicateBorder(self, x1, y1, x2, y2, Image())

	#### Face detection functions
	def DetectEyes(self, facePosition=None): return FSDK.DetectEyes(self) if facePosition is None else FSDK.DetectEyesInRegion(self, facePosition)
	def DetectFace(self): return FSDK.DetectFace(self)
	def DetectMultipleFaces(self): return FSDK.DetectMultipleFaces(self)
	def DetectFacialFeatures(self, facePosition=None): return FSDK.DetectFacialFeatures(self) if facePosition is None else FSDK.DetectFacialFeaturesInRegion(self, facePosition)
	def GetFaceTemplate(self, facePosition=None): return FSDK.GetFaceTemplate(self) if facePosition is None else FSDK.GetFaceTemplateInRegion(self, facePosition)
	def DetectFacialAttributeUsingFeatures(self, features, attributeName): return FSDK.DetectFacialAttributeUsingFeatures(self, features, attributeName)

	#### special functions to work with image data
	def ImageData(self): return FSDK.GetImageData(self)
	if windows:
		def GetHBitmap(self): return FSDK.SaveImageToHBitmap(self)
	def ToBuffer(self, colorMode):
		buffer = bytes(FSDK._GetImageBufferSize(self, colorMode))
		FSDK._SaveImageToBuffer(self, buffer, colorMode)
		return buffer
	ToBytes = ToBuffer

class Tracker(ctypes.Structure):
	_fields_ = ("handle", c_int), # FSDK tracker handle (-1 means invalid or uninitialized handle)
	def __new__(cls, arg = None):
		if arg is None: return FSDK.CreateTracker()
		if type(arg) is int: 
			tracker = super(Tracker, cls).__new__(cls)
			tracker.handle = -1
			return tracker
		raise InvalidArgument('Tracker construction', const.FSDKE_INVALID_ARGUMENT, desc = str(arg))
	Free = __del__ = lambda self: FSDK.FreeTracker(self)
	__repr__ = __str__ = lambda x: 'Tracker(handle=%x)' % x.handle
	def Clear(self): FSDK.ClearTracker(self)
	
	def SetParameters(self, **kw):		
		if kw: FSDK.SetTrackerMultipleParameters(self, ';'.join('%s=%s'%(n, value_to_str(v)) for n,v in kw.items()))
	def SetParameter(self, paramName, paramValue): FSDK.SetTrackerParameter(self, paramName, value_to_str(paramValue))
	def SetMultipleParameters(self, params): FSDK.SetTrackerMultipleParameters(self, params)
	def GetParameter(self, parameterName): return FSDK.GetTrackerParameter(self, parameterName)	# return parameter value
	def FeedFrame(self, cameraIdx, img, maxIDs = 256): return FSDK.FeedFrame(self, cameraIdx, img, maxIDs = maxIDs) # return array of IDs
	def GetFacePosition(self, cameraIdx, ID): return FSDK.GetTrackerFacePosition(self, cameraIdx, ID) # return FacePosition
	def GetFacialFeatures(self, cameraIdx, ID): return FSDK.GetTrackerFacialFeatures(self, cameraIdx, ID)
	def GetEyes(self, cameraIdx, ID): return FSDK.GetTrackerEyes(self, cameraIdx, ID)
	def GetTrackerFacialAttribute(self, cameraIdx, ID, attributeName): return FSDK.GetTrackerFacialAttribute(self, cameraIdx, ID, attributeName)
	def LockID(self, ID): FSDK.LockID(self, ID)
	def UnlockID(self, ID): FSDK.UnlockID(self, ID)
	def PurgeID(self, ID): FSDK.PurgeID(self, ID)
	def GetName(self, ID): return FSDK.GetName(self, ID)
	def SetName(self, ID, name): FSDK.SetName(self, ID, name)
	def GetAllNames(self, ID): return FSDK.GetAllNames(self, ID)
	def GetIDReassignment(self, ID): return FSDK.GetIDReassignment(self, ID)
	def GetSimilarIDList(self, ID): return FSDK.GetSimilarIDList(self, ID)

	def SaveToFile(self, fileName): FSDK.SaveTrackerMemoryToFile(self, fileName)
	@staticmethod
	def FromFile(fileName): return FSDK.LoadTrackerMemoryFromFile(fileName)
	def GetMemory(self):
		buffer = bytes(FSDK._GetTrackerMemoryBufferSize(self))
		FSDK._SaveTrackerMemoryToBuffer(self, buffer)
		return buffer
	ToBytes = GetMemory
	@staticmethod
	def FromMemory(buffer): return FSDK.LoadTackerMemoryFromBuffer(buffer)
	FromBytes = FromMemory

# argument types by its names for type checking mechanism
arg_types = {
#	'facePosition': FacePosition,
	'eyeCoords': Eyes,
	'facialFeatures': Features,
	'tracker': Tracker,
	'camera': Camera,
	'sourceImage': Image,
	'destImage': Image,
	'image': Image,
	'faceTemplate': FaceTemplate,
	'faceTemplate1': FaceTemplate,
	'faceTemplate2': FaceTemplate,
}
if windows: arg_types['videoFormat'] = VideoFormatInfo

# python2&3 base class for FSDK wrapper functions
class FSDK_Wrapper:
	# generate a dictionary that accociates all error codes with their FSDK exceptions
	def get_all_fsdk_exceptions():
		import inspect
		ex = {name.upper():cls for name, cls in sys.modules[__name__].__dict__.items() if inspect.isclass(cls) and issubclass(cls, FSDK_Exception) and cls is not FSDK_Exception}
		for id, name in ERROR_NAMES.items():
			if id:
				errname = name[6:].replace("_", "")
				if errname in ex: yield (id, ex[errname])
				else: raise Exception("Failed to locate FSDK exception for error %s" % name)
				del ex[errname]
		if ex:
			raise Exception("Found exception class(es) without error code:\n%s" % '\n'.join('class ' + cls.__name__ for cls in ex.values()))
	FSDKErrors = dict(get_all_fsdk_exceptions())
	del get_all_fsdk_exceptions
	@staticmethod
	def prepare(dct):
		def get_key_wrapper(key, func):
			key = key.replace('__', '_')
			a_names = inspect.getargspec(func).args[1:]
			a_types = {ind: arg_types[pname] for ind, pname in enumerate(a_names) if pname in arg_types}
			try:
				fsdkFunc = getattr(fsdkDll, key)
			except AttributeError as ex:
				if not func.__doc__.startswith("FSDK_ver"):
					raise ex
				def missed_function(message):
					def error(*v, **kw):
						raise Exception(message)
					return error
				fsdkFunc = missed_function("The function '%s' requires FaceSDK version %s or later" % (key, func.__doc__.split()[1]))

			def fsdk_wrapper(self, *arg, **kw):
				def fsdk_caller(*arg, **kw):
					for ind, req_type in a_types.items():
						if type(arg[ind]) is not req_type:
							self.lastErrorID = const.FSDKE_INVALID_ARGUMENT
							self.lastError = InvalidArgument(key, self.lastErrorID, "type(%s) must be '%s', not '%s'" % (a_names[ind], req_type.__name__, type(arg[ind]).__name__))
							raise self.lastError
					self.lastErrorID = res = fsdkFunc(*arg)
					if res:
						self.lastError = FSDK_Wrapper.FSDKErrors.get(res, FSDK_Exception)(key, res)
						if kw and kw.get('skip') in {res, all}: return None
						raise self.lastError
					else: self.lastError = None
					if kw and 'post' in kw: kw['post'](self)
					return True
				return func(fsdk_caller, *arg, **kw)
			return fsdk_wrapper

		# generate callable FSDK functions
		items = [(k,v) for k, v in dct.items() if k.startswith('FSDK_') and callable(v)]
		for name, func in items:
			del dct[name]
			func = get_key_wrapper(name, func) # remove 'FSDK_' prefix
			if func:
				dct[name[5:]] = func

		# copy constants from const.py module to this class
		dct.update((item, getattr(const, item)) for item in dir(const) if not item.startswith('__'))

		# copy base and windows specific types to this class
		items = Image, Point, FacePosition, Eyes, Camera, FaceTemplate, Features, Tracker
		if windows: items += (win.HBITMAP, VideoFormatInfo)
		dct.update((cls.__name__, cls) for cls in items)

		# make FSDK_Exception to be FSDK.Exception
		dct['Exception'] = FSDK_Exception
		# copy all exceptions to the FSDK namespace
		for ex in FSDK_Wrapper.FSDKErrors.values(): dct[ex.__name__] = ex

# decorator for new functions of new versions of FaceSDK
def FSDK_ver(ver):
	def wrapper(f):
		def caller(*args, **kw): f(*args, **kw)
		setattr(caller, "__doc__", "FSDK_ver %s" % ver)
		return caller
	return wrapper

# class for definition of FSDK wrapper functions
class FSDK_Class(FSDK_Wrapper):
	activated = False
	__bool__ = lambda self: self.activated # True if FSDK library is activated

	lastErrorID = const.FSDKE_OK
	lastError = None # the last FSDK_Exception object
	char_buffer = (c_char*4096)() # internal buffer used to exchange data with external __cdecl functions

	@classmethod
	def receive_string(cls, func):
		while 1:
			try:
				func(cls.char_buffer)
				return cls.char_buffer.value.decode('utf-8')
			except FSDKE_InsufficientBufferSize: cls.char_buffer = (c_char*(2*len(cls.char_buffer)))()

	##### Initialization functions #####
	def FSDK_ActivateLibrary(f, licenseKey): f(create_string_buffer(licenseKey.encode('utf-8')), post = lambda self: setattr(FSDK_Class, 'activated', True))
	def FSDK_GetHardware_ID(f): f(FSDK_Class.char_buffer); return FSDK_Class.char_buffer.value.decode('utf-8')
	def FSDK_GetLicenseInfo(f): f(FSDK_Class.char_buffer); return FSDK_Class.char_buffer.value.decode('utf-8')
	def FSDK_GetNumThreads(f): i = c_int(); f(byref(i)); return i.value
	def FSDK_SetNumThreads(f, num): f(c_int(num))
	def FSDK_Initialize(f, dataFilesPath=''): f(create_string_buffer(dataFilesPath.encode('utf-8')))
	def FSDK_Finalize(f): f()

	##### Face detection functions (available in Image class) #####
	def FSDK_DetectEyes(f, image): eyes=Eyes(); f(image, byref(eyes)); return eyes
	def FSDK_DetectEyesInRegion(f, image, facePosition): eyes=Eyes(); f(image, byref(facePosition), byref(eyes)); return eyes
	def FSDK_DetectFace(f, image): fp=FacePosition(); f(image, byref(fp)); return fp
	def FSDK_DetectMultipleFaces(f, image):
		max_faces, cnt = 256, c_int()
		while 1:
			fp = (FacePosition*max_faces)()
			if f(image, byref(cnt), fp, ctypes.sizeof(fp), skip=const.FSDKE_FACE_NOT_FOUND):
				if cnt.value < max_faces: return fp[:cnt.value]
			else: return ()
			max_faces *= 2
	def FSDK_DetectFacialFeatures(f, image, confidenceLevels = False):
		if confidenceLevels: return FSDK.DetectFacialFeaturesEx(image)
		ff = Features(); f(image, byref(ff)); return ff
	def FSDK_DetectFacialFeaturesInRegion(f, image, facePosition, confidenceLevels = False):
		if confidenceLevels: return FSDK.DetectFacialFeaturesEx(image, byref(facePosition))
		ff = Features(); f(image, byref(facePosition), byref(ff)); return ff
	def FSDK_DetectFacialFeaturesEx(f, image): ff = Features(); ff.confidenceLevels = ConfidenceLevels(); f(image, byref(ff), byref(ff.confidenceLevels)); return ff
	def FSDK_DetectFacialFeaturesInRegionEx(f, image, facePosition): ff = Features(); ff.confidenceLevels = ConfidenceLevels(); f(image, byref(facePosition), byref(ff), byref(ff.confidenceLevels)); return ff
	def FSDK_SetFaceDetectionParameters(f, handleArbitraryRotations, determineFaceRotationAngle, internalResizeWidth):
		f(c_bool(handleArbitraryRotations), c_bool(determineFaceRotationAngle), c_int(internalResizeWidth))
	def FSDK_SetFaceDetectionThreshold(f, threshold): f(c_int(threshold))
## NOT SUPPORTED ## int _FSDKIMPORT_ FSDK_ExtractFaceImage(HImage Image, FSDK_Features * FacialFeatures, int Width, int Height, HImage * ExtractedFaceImage, FSDK_Features * ResizedFeatures);
	def FSDK_GetDetectedFaceConfidence(f): i = c_int(); f(byref(i)); return i.value

	##### Image manipulation functions (available in Image class) #####
	def FSDK_CreateEmptyImage(f): img = Image(-1); f(byref(img)); return img
	if windows:
		def FSDK_LoadImageFromFileW(f, fileName): img = Image(-1); f(byref(img), ctypes.create_unicode_buffer(fileName)); return img
		def FSDK_SaveImageToFileW(f, image, fileName): f(image, ctypes.create_unicode_buffer(fileName))
		LoadImageFromFile = lambda *x: FSDK_Class.LoadImageFromFileW(*x)
		SaveImageToFile = lambda *x: FSDK_Class.SaveImageToFileW(*x)
		def FSDK_LoadImageFromHBitmap(f, bitmapHandle): img = Image(-1); f(byref(img), bitmapHandle); return img
		def FSDK_SaveImageToHBitmap(f, image): bitmapHandle = HBITMAP(); f(image, byref(bitmapHandle)); return bitmapHandle
	else: # not windows
		def FSDK_LoadImageFromFile(f, fileName): img = Image(-1); f(byref(img), create_string_buffer(fileName.encode('utf-8'))); return img
		def FSDK_SaveImageToFile(f, image, fileName): f(image, create_string_buffer(fileName.encode('utf-8')))
	def FSDK_LoadImageFromBuffer(f, buffer, width, height, scanLine, imageMode): img = Image(-1); f(byref(img), buffer, c_int(width), c_int(height), c_int(scanLine), c_int(imageMode)); return img
	def FSDK_LoadImageFromJpegBuffer(f, buffer, bufferLength=None): img = Image(-1); f(byref(img), buffer, c_uint(bufferLength or len(buffer))); return img
	def FSDK_LoadImageFromPngBuffer(f, buffer, bufferLength=None): img = Image(-1); f(byref(img), buffer, c_uint(bufferLength or len(buffer))); return img
	def FSDK_FreeImage(f, image):
		if image.handle != -1: f(image); image.handle = -1
	if True: # use Image.GetBuffer()
		def FSDK__GetImageBufferSize(f, image, imageMode): i = c_int(); f(image, byref(i), c_int(imageMode)); return i.value
		def FSDK__SaveImageToBuffer(f, image, buffer, imageMode): f(image, buffer, c_int(imageMode))
	def FSDK_SetJpegCompressionQuality(f, quality): f(c_int(quality))
	def FSDK_CopyImage(f, sourceImage, destImage): f(sourceImage, destImage); return destImage
	def FSDK_ResizeImage(f, sourceImage, ratio, destImage): f(sourceImage, c_double(ratio), destImage); return destImage
	def FSDK_ResizeImageXY(f, sourceImage, ratioX, ratioY, destImage): f(sourceImage, c_double(ratioX), c_double(ratioY), destImage); return destImage
	def FSDK_RotateImage90(f, sourceImage, multiplier, destImage): f(sourceImage, c_int(multiplier), destImage); return destImage
	def FSDK_RotateImage(f, sourceImage, angle, destImage): f(sourceImage, c_double(angle), destImage); return destImage
	def FSDK_RotateImageCenter(f, sourceImage, angle, xCenter, yCenter, destImage): f(sourceImage, c_double(angle), c_double(xCenter), c_double(yCenter), destImage); return destImage
	def FSDK_CopyRect(f, sourceImage, x1, y1, x2, y2, destImage): f(sourceImage, c_int(x1), c_int(y1), c_int(x2), c_int(y2), destImage); return destImage
	def FSDK_CopyRectReplicateBorder(f, sourceImage, x1, y1, x2, y2, destImage): f(sourceImage, c_int(x1), c_int(y1), c_int(x2), c_int(y2), destImage); return destImage
	def FSDK_MirrorImage(f, image, useVerticalMirroringInsteadOfHorizontal=False): f(image, c_bool(useVerticalMirroringInsteadOfHorizontal)); return image
	def FSDK_GetImageWidth(f, image): i = c_int(); f(image, byref(i)); return i.value
	def FSDK_GetImageHeight(f, image): i = c_int(); f(image, byref(i)); return i.value
	def FSDK_GetImageData(f, image):
		buf, width, height, scanLine, colorMode = POINTER(c_ubyte)(), c_int(), c_int(), c_int(), c_int()
		f(image, byref(buf), byref(width), byref(height), byref(scanLine), byref(colorMode))
		buf.width, buf.height, buf.scanLine, buf.colorMode = width.value, height.value, scanLine.value, colorMode.value
		return buf

	##### Matching (available in Image class) #####
	def FSDK_GetFaceTemplate(f, image): faceTemplate = FaceTemplate(); f(image, byref(faceTemplate)); return faceTemplate
	def FSDK_GetFaceTemplateInRegion(f, image, facePosition): faceTemplate = FaceTemplate(); f(image, byref(facePosition), byref(faceTemplate)); return faceTemplate
	def FSDK_GetFaceTemplateUsingFeatures(f, image, facialFeatures): faceTemplate = FaceTemplate(); f(image, facialFeatures, byref(faceTemplate)); return faceTemplate
	def FSDK_GetFaceTemplateUsingEyes(f, image, eyeCoords): faceTemplate = FaceTemplate(); f(image, eyeCoords, byref(faceTemplate)); return faceTemplate
	def FSDK_MatchFaces(f, faceTemplate1, faceTemplate2): similarity = c_float(); f(faceTemplate1, faceTemplate2, byref(similarity)); return similarity.value
	def FSDK_GetMatchingThresholdAtFAR(f, FARValue): threshold = c_float(); f(c_float(FARValue), byref(threshold)); return threshold.value
	def FSDK_GetMatchingThresholdAtFRR(f, FRRValue): threshold = c_float(); f(c_float(FRRValue), byref(threshold)); return threshold.value

	##### Webcam usage #####
	def FSDK_InitializeCapturing(f): f()
	def FSDK_FinalizeCapturing(f): f()
	def FSDK_SetHTTPProxy(f, serverNameOrIPAddress, port, userName, password):
		f(create_string_buffer(serverNameOrIPAddress.encode('utf-8')), c_ushort(port), create_string_buffer(userName.encode('utf-8')), create_string_buffer(password.encode('utf-8')))
	def FSDK_OpenIPVideoCamera(f, compression, URL, userName, password, timeoutSeconds): # compression type example: const.FSDK_MJPEG
		cam = Camera(); f(c_int(compression), create_string_buffer(URL.encode('utf-8')), create_string_buffer(userName.encode('utf-8')), create_string_buffer(password.encode('utf-8')), c_int(timeoutSeconds), byref(cam)); return cam
	def FSDK_CloseVideoCamera(f, camera):
		if camera.handle != -1: f(camera); camera.handle = -1
	def FSDK_GrabFrame(f, camera): im = Image(-1); f(camera, byref(im)); return im
	if windows:
		def FSDK_SetCameraNaming(f, useDevicePathAsName): f(c_bool(useDevicePathAsName))
		class CameraName(str):
			def __new__(cls, name, devicePath): inst = super(FSDK.CameraName, cls).__new__(cls, name); inst.devicePath = devicePath; return inst
		def ListCameraNames(self): 
			nl, pl = POINTER(ctypes.c_wchar_p)(), POINTER(ctypes.c_wchar_p)()
			n = self._GetCameraListEx(nl, pl)
			lst = [FSDK.CameraName(name, devicePath) for name, devicePath in zip(nl[:n], pl[:n])]
			self._FreeCameraList(nl, n)
			return lst
		def FSDK__GetCameraList(f, nameList): n = c_int(); f(byref(nameList), byref(n)); return n.value
		def FSDK__GetCameraListEx(f, nameList, pathList): n = c_int(); f(byref(nameList), byref(pathList), byref(n)); return n.value
		def FSDK__FreeCameraList(f, cameraList, cameraCount): f(cameraList, cameraCount)

		def ListVideoFormats(self, cameraName):
			vfl = POINTER(VideoFormatInfo)()
			lst = [VideoFormatInfo(f.Width, f.Height, f.BPP) for f in vfl[:self._GetVideoFormatList(cameraName, vfl)]]
			self._FreeVideoFormatList(vfl)
			return lst
		def FSDK__GetVideoFormatList(f, cameraName, videoFormatList): cnt = c_int(); f(ctypes.create_unicode_buffer(cameraName), byref(videoFormatList), byref(cnt)); return cnt.value
		def FSDK__FreeVideoFormatList(f, videoFormatList): f(videoFormatList)

		def FSDK_SetVideoFormat(f, cameraName, videoFormat): f(ctypes.create_unicode_buffer(cameraName), videoFormat)
		def FSDK_OpenVideoCamera(f, cameraName): c = Camera(); f(ctypes.create_unicode_buffer(cameraName), byref(c)); return c

	##### Tracker #####
	def FSDK_CreateTracker(f): tr = Tracker(-1); f(byref(tr)); return tr
	def FSDK_FreeTracker(f, tracker):
		if tracker.handle != -1: f(tracker); tracker.handle = -1
	def FSDK_ClearTracker(f, tracker): f(tracker)
	def FSDK_SetTrackerParameter(f, tracker, parameterName, parameterValue): f(tracker, create_string_buffer(parameterName.encode('utf-8')), create_string_buffer(value_to_str(parameterValue).encode('utf-8')))
	def FSDK_SetTrackerMultipleParameters(f, tracker, parameters):
		err_pos = c_int(); f(tracker, create_string_buffer(parameters.encode('utf-8')), byref(err_pos), skip=all)
		if FSDK.lastErrorID:
			raise FSDK_Wrapper.FSDKErrors.get(FSDK.lastErrorID, FSDK_Exception)('FSDK_SetTrackerMultipleParameters', FSDK.lastErrorID, "in line '%s' at position = %s" % (parameters, err_pos.value))
	def FSDK_GetTrackerParameter(f, tracker, parameterName): 
		return FSDK_Class.receive_string(lambda buf: f(tracker, create_string_buffer(parameterName.encode('utf-8')), buf, c_longlong(len(buf))))

	def FeedFrame(self, tracker, cameraIdx, image, maxIDs = 256):
		buf = (c_longlong*maxIDs)(); faceCount = c_longlong()
		self._FeedFrame(tracker, c_longlong(cameraIdx), image, byref(faceCount), buf, c_longlong(maxIDs*8))
		return buf[:faceCount.value]
	def FSDK__FeedFrame(f, tracker, cameraIdx, image, faceCount, IDs, maxSizeInBytes): f(tracker, cameraIdx, image, faceCount, IDs, maxSizeInBytes)
	def FSDK_GetTrackerEyes(f, tracker, cameraIdx, ID): eyes=Eyes(); f(tracker, c_longlong(cameraIdx), c_longlong(ID), byref(eyes)); return eyes
	def FSDK_GetTrackerFacialFeatures(f, tracker, cameraIdx, ID): ff = Features(); f(tracker, c_longlong(cameraIdx), c_longlong(ID), byref(ff)); return ff
	def FSDK_GetTrackerFacePosition(f, tracker, cameraIdx, ID): fp = FacePosition(); f(tracker, c_longlong(cameraIdx), c_longlong(ID), byref(fp)); return fp
	def FSDK_GetTrackerFacialAttribute(f, tracker, cameraIdx, ID, attributeName):		
		res = FSDK_Class.receive_string(lambda buf: f(tracker, c_longlong(cameraIdx), c_longlong(ID), create_string_buffer(attributeName.encode('utf-8')), buf, c_longlong(len(buf)), skip = const.FSDKE_UNKNOWN_ATTRIBUTE))
		if FSDK.lastErrorID:
			raise FSDK_Wrapper.FSDKErrors.get(FSDK.lastErrorID, FSDK_Exception)("FSDK_GetTrackerFacialAttribute", FSDK.lastErrorID, "'%s'" % attributeName)
		return res
	def FSDK_LockID(f, tracker, ID): f(tracker, c_longlong(ID))
	def FSDK_UnlockID(f, tracker, ID): f(tracker, c_longlong(ID))
	def FSDK_PurgeID(f, tracker, ID): f(tracker, c_longlong(ID))
	def FSDK_GetName(f, tracker, ID): return FSDK_Class.receive_string(lambda buf: f(tracker, c_longlong(ID), buf, c_longlong(len(buf))))
	def FSDK_SetName(f, tracker, ID, name): f(tracker, c_longlong(ID), create_string_buffer(name.encode('utf-8')))
	def FSDK_GetIDReassignment(f, tracker, ID): rID = c_longlong(); f(tracker, c_longlong(ID), byref(rID)); return rID.value
	def FSDK_GetSimilarIDList(f, tracker, ID):
		lst = (c_longlong*FSDK.GetSimilarIDCount(tracker, ID))()
		f(tracker, ID, lst, c_longlong(len(lst)*8))
		return lst
	def FSDK_GetSimilarIDCount(f, tracker, ID): count = c_longlong(); f(tracker, c_longlong(ID), byref(count)); return count.value
	def FSDK_GetAllNames(f, tracker, ID):
		return FSDK_Class.receive_string(lambda buf: f(tracker, ID, buf, c_longlong(len(buf)))).split(';')
	def FSDK_SaveTrackerMemoryToFile(f, tracker, fileName): f(tracker, create_string_buffer(fileName.encode('utf-8')))
	def FSDK_LoadTrackerMemoryFromFile(f, fileName): tr = Tracker(-1); f(byref(tr), create_string_buffer(fileName.encode('utf-8'))); return tr
	if True: ### use Tracker.GetMemory() instead of the following two functions
		def FSDK__GetTrackerMemoryBufferSize(f, tracker): i = c_longlong(); f(tracker, byref(i)); return i.value
		def FSDK__SaveTrackerMemoryToBuffer(f, tracker, buffer): f(tracker, buffer, c_longlong(len(buffer)))
	def FSDK_LoadTrackerMemoryFromBuffer(f, buffer): tr = Tracker(-1); f(byref(tr), buffer); return tr

	##### Facial attributes #####
	def FSDK_DetectFacialAttributeUsingFeatures(f, image, facialFeatures, attributeName):
		attr_name = create_string_buffer(attributeName.encode('utf-8'))
		return FSDK_Class.receive_string(lambda buf: f(image, features, attr_name, buf, c_longlong(len(buf)))) # should we convert the string values into the dict ?
	def FSDK_GetValueConfidence(f, attributeValues, value):
		conf = c_float(); f(create_string_buffer(attributeValues.encode('utf-8')), create_string_buffer(value.encode('utf-8')), byref(conf)); return conf.value

	@FSDK_ver("7.2")
	def FSDK_SetParameters(f, values='', **kwargs):
		err_pos, parameters = c_int(), values.rstrip()
		if kwargs:
			if parameters and not parameters.endswith(';'):
				parameters += ';'
			parameters += ';'.join('%s=%s' % (n, value_to_str(v)) for n, v in kwargs.items())
		f(create_string_buffer(parameters.encode('utf-8')), byref(err_pos), skip=all)
		if FSDK.lastErrorID:
			raise FSDK_Wrapper.FSDKErrors.get(FSDK.lastErrorID, FSDK_Exception)("FSDK_SetParameters", FSDK.lastErrorID, "in line '%s' at position = %s" % (parameters, err_pos.value))

	@FSDK_ver("7.2")
	def FSDK_SetParameter(f, name, value):
		f(create_string_buffer(name.encode('utf-8')), create_string_buffer(value_to_str(value).encode('utf-8')))

	FSDK_Wrapper.prepare(locals())
	del FSDK_Wrapper.prepare

FSDK = FSDK_Class()
