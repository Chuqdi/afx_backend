import { PrismaService } from 'nestjs-prisma';

const prisma = new PrismaService();

(async () => {
  try {
    await prisma.user.deleteMany();
    console.log('Deleted records in user table');

    await prisma.affirmation.deleteMany();
    console.log('Deleted records in affirmation table');

    await prisma.library.deleteMany();
    console.log('Deleted records in library table');

    await prisma.package.deleteMany();
    console.log('Deleted records in package table');
  } catch (e) {
    console.error(e);
    process.exit(1);
  } finally {
    await prisma.$disconnect();
  }
})();
