/*
 *   Copyright (C) 2009 Andrew Coles <andrew_coles@yahoo.co.uk>
 *   Copyright (C) 2009 Kristof Bal <kristof.bal@gmail.com>
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU Library General Public License as
 *   published by the Free Software Foundation; either version 2, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details
 *
 *   You should have received a copy of the GNU Library General Public
 *   License along with this program; if not, write to the
 *   Free Software Foundation, Inc.,
 *   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 */

#include "conversioni18ncatalog.h"
#include <QMutex>
#include <kglobal.h>
#include <klocale.h>

static bool catalogLoaded = false;
static QMutex loadingMutex;

void Conversioni18nCatalog::loadCatalog() {

	loadingMutex.lock();
	if (!catalogLoaded) {
		KGlobal::locale()->insertCatalog("libconversion");
		catalogLoaded = true;
	}
	loadingMutex.unlock();
}
