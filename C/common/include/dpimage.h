#ifndef _DPIMAGE_H
#define _DPIMAGE_H
/*
 * Fledge
 *
 * Copyright (c) 2021 Dianomic Systems
 *
 * Released under the Apache 2.0 Licence
 *
 * Author: Mark Riddoch
 */

/**
 * Simple Image class that will be used within data points to store image data.
 *
 * This class merely acts to encapsulate the data of a simple image in memory, 
 * compelx functionality will be supported elsewhere. Images within the class
 * are stored as a simple, single area of memory the size of which is defined
 * by the width, hieght and depth of the image.
 */
class DPImage {
	public:
		DPImage(int width, int height, int depth, void *data);
		DPImage(const DPImage& rhs);
		DPImage& operator=(const DPImage& rhs);
		~DPImage();
		/**
		 * Return the height of the image
		 */
		int		getHeight() { return m_height; };
		/**
		 * Return the width of the image
		 */
		int		getWidth() { return m_width; };
		/**
		 * Return the depth of the image in bits
		 */
		int		getDepth() { return m_depth; };
		/**
		 * Return a pointer to the raw data of the image
		 */
		void		*getData() { return m_pixels; };
	protected:
		int		m_width;
		int		m_height;
		int		m_depth;
		void		*m_pixels;
		int		m_byteSize;
};

#endif
