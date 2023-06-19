import { PrismaService } from 'nestjs-prisma';
import { packages, libraries, categories, affirmations } from './mock';

const prisma = new PrismaService();

(async () => {
  try {
    await prisma.affirmation.deleteMany({});
    console.log('Deleted recodes in affirmation table');

    await prisma.category.deleteMany({});
    console.log('Deleted recodes in category table');

    await prisma.library.deleteMany({});
    console.log('Deleted recodes in library table');

    await prisma.package.deleteMany({});
    console.log('Deleted recodes in package table');

    const packageIds = [];
    const libraryIds = [];
    const categoryIds = [];

    for (let i = 0; i < packages.length; i++) {
      const result = await prisma.package.create({
        data: packages[i],
      });
      if (result.id) packageIds.push(result.id);
    }
    console.log('Created new recodes in package table');

    for (let i = 0; i < libraries.length; i++) {
      const result = await prisma.library.create({
        data: {
          ...libraries[i],
          packageId: packageIds[0],
        },
      });
      if (result.id) libraryIds.push(result.id);
    }
    console.log('Created new recodes in library table');

    for (let i = 0; i < categories.length; i++) {
      const result = await prisma.category.create({
        data: {
          ...categories[i],
          libraryId: libraryIds[0],
        },
      });
      if (result.id) categoryIds.push(result.id);
    }
    console.log('Created new recodes in library table');

    for (let i = 0; i < affirmations.length; i++) {
      const result = await prisma.affirmation.create({
        data: {
          ...affirmations[i],
          libraryId: libraryIds[0],
          categoryId: categoryIds[0],
          packageId: packageIds[0],
          userId: packageIds[1],
        },
      });
      if (result.id) categoryIds.push(result.id);
    }
    console.log('Created new recodes in affirmation table');
  } catch (e) {
    console.error(e);
    process.exit(1);
  } finally {
    await prisma.$disconnect();
  }
})();
